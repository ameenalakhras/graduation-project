from django.contrib import admin
from classroom.models import ClassRoom, Post, Comments, Material, \
                             TaskSolution, Task, TaskSOlutionInfo

admin.site.register(ClassRoom)
admin.site.register(Post)
admin.site.register(TaskSolution)
admin.site.register(Task)
admin.site.register(TaskSOlutionInfo)
admin.site.register(Comments)
admin.site.register(Material)
