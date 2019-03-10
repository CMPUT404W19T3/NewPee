# Create your views here.
# def post_create_view(request):
#     form = PostForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         form = PostForm()

#     context = {
#         'form': form
#     }
#     return render(request, "", context)

# def post_modal_view(request, id):
#     obj = Post.objects.get(id=1)
#     context = {
#         'object': obj
#     }
#     return render(request, "", context)

# def product_list_view(request, id):
#     queryset = Post.objects.all()    # list of objects
#     context = {
#         "object_list": queryset
#     }
#     return render(request, "", context)
