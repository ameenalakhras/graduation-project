class ClassRoomSerializer(serializers.ModelSerializer):
        class Meta:
            model = ClassRoom
            fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comments
            fields = '__all__'

# the task serializer should make sure it's a teacher who is making the task
class TaskSerializer(serializers.ModelSerializer):
        class Meta:
            model = Task
            fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = '__all__'

class ClassRoomTeacherSerializer(serializers.ModelSerializer):
        class Meta:
            model = ClassRoomTeacher
            fields = '__all__'
