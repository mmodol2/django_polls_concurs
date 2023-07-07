from django.contrib import admin

from .models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ('User', {'fields': ('user',)}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "pub_date", "user", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    # fields = ["pub_date", "question_text"]

    def get_form(self, request, obj=None, **kwargs):
            form = super().get_form(request, obj, **kwargs)
            form.base_fields['user'].initial = request.user.id
            return form

admin.site.register(Question, QuestionAdmin)

# admin.site.register(Question)
# admin.site.register(Choice)
