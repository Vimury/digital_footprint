let start = new Date()

function check_time(){
    let now = new Date()
    let diff = now - start
    console.log(diff)
//    if(diff >= 1000){
//        start = now
//    }
}


setInterval(check_time(), 1000);

