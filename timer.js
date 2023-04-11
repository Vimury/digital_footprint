<script>
    let work_time = 30;
    let a = new Date();
    let $timer = $('timer');
    function check_time()
    {
        let b = new Date();
        let diff = Math.round((b - a) / 1000);
        return diff;
    }

    function display(){
        let sum = work_time - check_time();
        console.log(sum);
        if(sum>=0) {
            let mins = Math.floor(sum / 60), secs = Math.floor(sum % 60);
            if($timer[0]) {
                $timer[0].innerHTML = Math.floor(mins / 10) + (mins % 10) + ':' + Math.floor(secs / 10) + (secs % 10);
            }
        } else {
            $timer[0].innerHTML = "TIME IS UP!";
            clearInterval(time);
        }
    }
    display();
    let time = setInterval(display,1000);
</script>