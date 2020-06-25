from django.contrib import admin
from classroom.models import ClassRoom, Post, Comments, Material, \
                             TaskSolution, Task, TaskSOlutionInfo
                             # ClassRoomTeacher, ClassRoomStudent

# admin.site.register(ClassRoomStudent)
admin.site.register(ClassRoom)
admin.site.register(Post)
admin.site.register(TaskSolution)
admin.site.register(Task)
admin.site.register(TaskSOlutionInfo)
admin.site.register(Comments)
admin.site.register(Material)
# admin.site.register(ClassRoomTeacher)

