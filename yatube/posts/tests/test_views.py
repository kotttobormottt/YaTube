from django.test import Client, TestCase
from django.urls import reverse

from ..models import Follow, Group, Post, User


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.user_two = User.objects.create_user(username='TestUser2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание группы'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст поста',
            author=cls.user,
            group=cls.group
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def check_post_info(self, post):
        with self.subTest(post=post):
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author, self.post.author)
            self.assertEqual(post.group.id, self.post.group.id)

    def test_groups_page_show_correct_context(self):
        """Шаблон group_list.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug})
        )
        self.assertEqual(response.context['group'], self.group)
        self.check_post_info(response.context['page_obj'][0])

    def test_profile_page_show_correct_context(self):
        """Шаблон profile.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.context['author'], self.user)
        self.check_post_info(response.context['page_obj'][0])

    def test_detail_page_show_correct_context(self):
        """Шаблон post_detail.html сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        self.check_post_info(response.context['post'])

    def test_follow_page_(self):
        """Авторизированный автор может подписаться на другого автора."""
        follow_count = Follow.objects.count()
        self.authorized_client.post(
            reverse('posts:profile_follow',
                    kwargs={"username": str(PostPagesTests.user_two)},)
        )
        self.assertEqual(Follow.objects.count(), follow_count + 1)
        self.assertTrue(
            Follow.objects.filter(
                user=PostPagesTests.user, author=PostPagesTests.user_two
            ).exists()
        )

    def test_unfollow_page_(self):
        """Авторизированный автор может отписаться от избранного автора."""
        self.authorized_client.post(
            reverse('posts:profile_follow',
                    kwargs={"username": str(PostPagesTests.user_two)},)
        )
        follow_count = Follow.objects.count()
        self.authorized_client.post(
            reverse('posts:profile_unfollow',
                    kwargs={"username": str(PostPagesTests.user_two)},)
        )
        self.assertEqual(Follow.objects.count(), follow_count - 1)
        self.assertFalse(
            Follow.objects.filter(
                user=PostPagesTests.user, author=PostPagesTests.user_two
            ).exists()
        )

    def test_follow_index_page_(self):
        """Новая запись пользователя появляется в ленте followers и
        не появляется в ленте остальных."""
        new_user = User.objects.create_user(username='TestFollow')
        new_client = Client()
        new_client.force_login(new_user)
        new_client.post(
            reverse('posts:profile_follow',
                    kwargs={"username": str(PostPagesTests.user_two)},)
        )
        new_post = Post.objects.create(
            author=PostPagesTests.user_two,
            text='Текст для теста follow',
        )
        response = self.authorized_client.get(reverse('posts:follow_index'))
        response_new_user = new_client.get(reverse('posts:follow_index'))
        self.assertIn(
            new_post,
            response_new_user.context["page_obj"].object_list
        )
        self.assertNotIn(new_post, response.context["page_obj"].object_list)


class PaginatorViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.group_list = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание группы'
        )
        post_list = []
        for i in range(0, 13):
            new_post = Post(
                text=f'Тестовый пост контент {i}',
                group=cls.group_list,
                author=cls.user
            )
            post_list.append(new_post)
        Post.objects.bulk_create(post_list)

    def test_first_page(self):
        """Тестируем первую страницу пагинатора."""
        slug = self.group_list.slug
        username = self.user.username
        page_list = [
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': slug}),
            reverse('posts:profile', kwargs={'username': username})
        ]
        for page in page_list:
            response = self.authorized_client.get(page)
            self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page(self):
        """Тестируем вторую страницу пагинатора."""
        slug = self.group_list.slug
        username = self.user.username
        page_list = {
            reverse('posts:index'),
            reverse('posts:group_list', kwargs={'slug': slug}),
            reverse('posts:profile', kwargs={'username': username})
        }
        count_posts = Post.objects.count()
        count = count_posts - 10
        for page in page_list:
            response = self.authorized_client.get(page + '?page=2')
            self.assertEqual(len(response.context['page_obj']), count)
