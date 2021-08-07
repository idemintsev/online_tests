<script>
    var user_choices = [];

    function UserAnswer(choice) {
        user_answer = choice.value;
        if (user_choices.includes(user_answer)) {
            for(i=0; i < user_choices.length; i++) {
                if (user_answer == user_choices[i]) {
                    alert('До удаления' + user_choices);
                    user_choices.splice(i, 1);
                    alert('После удаления' + user_choices);
                }
            }
        } else {
            alert('До добавления' + user_choices);
            user_choices.push(choice.value);
            alert('После добавления' + user_choices);
        }
    }
</script>
