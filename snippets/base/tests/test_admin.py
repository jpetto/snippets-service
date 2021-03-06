from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from unittest.mock import Mock, patch

from snippets.base.admin import ASRSnippetAdmin, SnippetAdmin, SnippetTemplateAdmin
from snippets.base.models import (STATUS_CHOICES, ASRSnippet, Snippet,
                                  SnippetTemplate, SnippetTemplateVariable)
from snippets.base.tests import (ASRSnippetFactory, SnippetTemplateFactory,
                                 SnippetTemplateVariableFactory, TestCase, UserFactory)


class SnippetAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = SnippetAdmin(Snippet, None)
        self.model_admin.admin_site = Mock()
        self.user = User.objects.get_or_create(username='foo', email='foo@example.com')[0]

    def test_save_as_published(self):
        request = self.factory.post('/', data={
            'name': 'test',
            'template': 'foo',
            'published': 'on',
            'ready_for_review': 'on',
            '_saveasnew': True
        })
        request.user = self.user

        with patch('snippets.base.admin.admin.ModelAdmin.change_view') as change_view_mock:
            self.model_admin.change_view(request, 999)
            change_view_mock.assert_called_with(request, 999, '', None)
            request = change_view_mock.call_args[0][0]
            self.assertTrue('published' not in request.POST)
            self.assertTrue('ready_for_review' not in request.POST)

    def test_normal_save_published(self):
        """Test that normal save doesn't alter 'published' attribute."""
        request = self.factory.post('/', data={
            'name': 'test',
            'template': 'foo',
            'ready_for_review': 'foo',
            'published': 'foo'
        })
        request.user = self.user

        with patch('snippets.base.admin.admin.ModelAdmin.change_view') as change_view_mock:
            self.model_admin.change_view(request, 999)
            change_view_mock.assert_called_with(request, 999, '', None)
            request = change_view_mock.call_args[0][0]
            self.assertEqual(request.POST['published'], 'foo')
            self.assertEqual(request.POST['ready_for_review'], 'foo')


class SnippetTemplateAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = SnippetTemplateAdmin(SnippetTemplate, None)

    def _save_related(self, template):
        """
        Call SnippetTemplateAdmin.save_related for the given template instance.

        :returns:
            A list of the new template variables after save_related was called.
        """
        request = self.factory.post('/url', {})
        ModelForm = self.model_admin.get_form(request)

        form = ModelForm(instance=template)
        form.save_m2m = Mock()  # Called by save_related but unnecessary here.
        self.model_admin.save_related(request, form, [], True)

        return [variable.name for variable in
                SnippetTemplateVariable.objects.filter(template=template)]

    def test_save_related_add_new(self):
        """
        save_related should add new TemplateVariables for any new variables in
        the template code.
        """
        template = SnippetTemplateFactory.create(code="""
            <p>Testing {{ sample_var }}</p>
            {% if not another_test_var %}
              <p>Blah</p>
            {% endif %}
        """)
        variables = self._save_related(template)
        self.assertEqual(len(variables), 2)
        self.assertTrue('sample_var' in variables)
        self.assertTrue('another_test_var' in variables)

    def test_save_related_remove_old(self):
        """
        save_related should delete TemplateVariables that don't exist in the
        saved template anymore.
        """
        template = SnippetTemplateFactory.create(code="""
            <p>Testing {{ sample_var }}</p>
            {% if not another_test_var %}
              <p>Blah</p>
            {% endif %}
        """)
        SnippetTemplateVariableFactory.create(
            name='does_not_exist', template=template)
        SnippetTemplateVariableFactory.create(
            name='does_not_exist_2', template=template)

        self.assertTrue(SnippetTemplateVariable.objects
                        .filter(template=template, name='does_not_exist').exists())
        self.assertTrue(SnippetTemplateVariable.objects
                        .filter(template=template, name='does_not_exist_2').exists())

        variables = self._save_related(template)
        self.assertEqual(len(variables), 2)
        self.assertTrue('sample_var' in variables)
        self.assertTrue('another_test_var' in variables)

        self.assertFalse(SnippetTemplateVariable.objects
                         .filter(template=template, name='does_not_exist').exists())

        self.assertFalse(SnippetTemplateVariable.objects
                         .filter(template=template, name='does_not_exist_2').exists())

    @patch('snippets.base.admin.adminmodels.RESERVED_VARIABLES', ('reserved_name',))
    def test_save_related_reserved_name(self):
        """
        save_related should not add new TemplateVariables for variables that
        are in the RESERVED_VARIABLES list.
        """
        template = SnippetTemplateFactory.create(code="""
            <p>Testing {{ reserved_name }}</p>
            {% if not another_test_var %}
              <p>Blah</p>
            {% endif %}
        """)
        variables = self._save_related(template)
        self.assertEqual(len(variables), 1)
        self.assertTrue('another_test_var' in variables)

        self.assertFalse(SnippetTemplateVariable.objects
                         .filter(template=template, name='reserved_name').exists())


class ASRSnippetAdminTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.model_admin = ASRSnippetAdmin(ASRSnippet, None)
        self.model_admin.admin_site = Mock()
        self.user = UserFactory()

    def test_save_as_published(self):
        request = self.factory.post('/', data={
            'name': 'test',
            'template': 'foo',
            'status': STATUS_CHOICES['Published'],
            '_saveasnew': True
        })
        request.user = self.user

        with patch('snippets.base.admin.admin.ModelAdmin.change_view') as change_view_mock:
            self.model_admin.change_view(request, 999)
            change_view_mock.assert_called_with(request, 999)
            request = change_view_mock.call_args[0][0]
            self.assertEqual(request.POST['status'], STATUS_CHOICES['Draft'])

    def test_normal_save_published(self):
        """Test that normal save doesn't alter `status` attribute."""
        request = self.factory.post('/', data={
            'name': 'test',
            'template': 'foo',
            'status': STATUS_CHOICES['Published'],
        })
        request.user = self.user

        with patch('snippets.base.admin.admin.ModelAdmin.change_view') as change_view_mock:
            self.model_admin.change_view(request, 999)
            change_view_mock.assert_called_with(request, 999)
            request = change_view_mock.call_args[0][0]
            self.assertEqual(request.POST['status'], str(STATUS_CHOICES['Published']))

    def test_get_readonly_fields(self):
        asrsnippet = ASRSnippetFactory()
        request = self.factory.get('/')
        admin = ASRSnippetAdmin(ASRSnippet, AdminSite())

        # Not Super User
        request.user = UserFactory(is_superuser=False)
        readonly_fields = admin.get_readonly_fields(request, asrsnippet)
        self.assertTrue('for_qa' in readonly_fields)

        # SuperUser
        request.user = UserFactory(is_superuser=True)
        readonly_fields = admin.get_readonly_fields(request, asrsnippet)
        self.assertTrue('for_qa' not in readonly_fields)

    def test_get_queryset(self):
        snippets = ASRSnippetFactory.create_batch(2)
        qa_snippets = ASRSnippetFactory.create_batch(2, for_qa=True)
        request = self.factory.get('/')
        admin = ASRSnippetAdmin(ASRSnippet, AdminSite())

        # Not Super User
        request.user = UserFactory(is_superuser=False)
        queryset = admin.get_queryset(request)
        self.assertEqual(set(snippets), set(queryset.all()))

        # SuperUser
        request.user = UserFactory(is_superuser=True)
        queryset = admin.get_queryset(request)

        self.assertEqual(set(snippets + qa_snippets), set(queryset.all()))

    def test_make_published(self):
        to_be_published = ASRSnippetFactory.create_batch(2, status=STATUS_CHOICES['Draft'])
        already_published = ASRSnippetFactory(status=STATUS_CHOICES['Published'])
        ASRSnippetFactory.create_batch(2, status=STATUS_CHOICES['Draft'])

        queryset = ASRSnippet.objects.filter(id__in=[
            to_be_published[0].id,
            to_be_published[1].id,
            already_published.id
        ])

        with patch('snippets.base.admin.adminmodels.messages.warning') as warning:
            with patch('snippets.base.admin.adminmodels.messages.success') as success:
                ASRSnippetAdmin(ASRSnippet, None).make_published(None, queryset)

        self.assertEqual(
            set(ASRSnippet.objects.filter(status=STATUS_CHOICES['Published'])),
            set(to_be_published + [already_published])
        )
        self.assertTrue(warning.called)
        self.assertTrue(success.called)
