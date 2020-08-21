from Blog.models import Post,Comments
from django import forms

class PostForm(forms.ModelForm):
    
    class Meta:
        model=Post
        fields=('auther','title','text')

        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }


class CommentsForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ("auther","text")

        widgets={
            'auther':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }




    
