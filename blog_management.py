from abc import ABC, abstractmethod

# 1. Class: User
class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.__password = password  # Private attribute

    # Getter for password
    def get_password(self):
        return self.__password
    
    # Setter for password
    def set_password(self, new_password):
        self.__password = new_password

    # Basic representation
    def __str__(self):
        return f"User: {self.name}, Email: {self.email}"

# 2. Abstract Class: PostManager
class PostManager(ABC):
    @abstractmethod
    def create_post(self, title, content):
        pass
    
    @abstractmethod
    def edit_post(self, post, new_title, new_content):
        pass
    
    @abstractmethod
    def delete_post(self, post):
        pass

# 3. Class: Admin (inherits User)
class Admin(User, PostManager):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
    
    # Admin can manage all posts
    def create_post(self, title, content):
        return Post(title, content, self.name)

    def edit_post(self, post, new_title, new_content):
        post.title = new_title
        post.content = new_content
        print(f"Post '{post.title}' edited by Admin")

    def delete_post(self, post):
        print(f"Admin deleted post: {post.title}")
        del post

# 4. Class: Author (inherits User, implements PostManager)
class Author(User, PostManager):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)
        self.posts = []  # Author can manage their own posts
    
    # Author can create a post
    def create_post(self, title, content):
        post = Post(title, content, self.name)
        self.posts.append(post)
        return post
    
    # Author can edit their own posts
    def edit_post(self, post, new_title, new_content):
        if post.author == self.name:
            post.title = new_title
            post.content = new_content
            print(f"Post '{post.title}' edited by Author")
        else:
            print("Error: You can only edit your own posts.")

    # Author can delete their own posts
    def delete_post(self, post):
        if post.author == self.name:
            print(f"Author deleted their post: {post.title}")
            self.posts.remove(post)
            del post
        else:
            print("Error: You can only delete your own posts.")

# 5. Class: Post
class Post:
    def __init__(self, title, content, author):
        self.title = title
        self.content = content
        self.author = author
    
    # Magic method to return a user-friendly representation of the post
    def __str__(self):
        return f"Post Title: {self.title}\nAuthor: {self.author}\nContent: {self.content}"

    # Magic method to return the word count of the content
    def __len__(self):
        return len(self.content.split())

# Example Usage

def main():
    # Creating an Admin user
    admin = Admin("Admin User", "admin@blog.com", "adminpass")
    print(admin)

    # Creating an Author user
    author = Author("Author User", "author@blog.com", "authorpass")
    print(author)

    # Admin creates a post
    admin_post = admin.create_post("Admin's First Post", "This is an admin post.")
    print(admin_post)
    print(f"Word count: {len(admin_post)} words")

    # Author creates a post
    author_post = author.create_post("Author's First Post", "This is an author's post.")
    print(author_post)
    print(f"Word count: {len(author_post)} words")

    # Admin edits a post
    admin.edit_post(admin_post, "Updated Admin's Post", "Updated content for admin post.")
    print(admin_post)

    # Author edits their post
    author.edit_post(author_post, "Updated Author's Post", "Updated content for author's post.")
    print(author_post)

    # Author tries to delete another author's post
    admin.delete_post(author_post)  # Admin can delete anyone's post
    author.delete_post(admin_post)  # Author can only delete their own post

if __name__ == "__main__":
    main()
