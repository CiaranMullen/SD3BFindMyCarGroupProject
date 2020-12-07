var alive_second = 0;
var heartbeat_rate = 5000;

var myChannel = "SD3b";

function keep_alive()
{
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null){
					var date = new Date();
					alive_second = date.getTime();
					var keep_alive_data = this.responseText;
					console.log(keep_alive_data);
					var json_data = this.responseText;
					var json_obj = JSON.parse(json_data);
					if(json_obj.motion == 1){
						document.getElementById("Motion_id").innerHTML = "Intruder Dectected";
					}
					else{
						document.getElementById("Motion_id").innerHTML = "All safe";
					}
				}
			}
		}
	};
	request.open("GET", "keep_alive", true);
	request.send(null);
	setTimeout('keep_alive()', heartbeat_rate);
}

function time(){
	var d = new Date();
	var current_sec = d.getTime();
	if(current_sec - alive_second > heartbeat_rate + 1000){
		document.getElementById("Connection_id").innerHTML = " Dead";
	}
	else{
		document.getElementById("Connection_id").innerHTML = " Alive";
	}
	setTimeout('time()', 1000);
}

function sendEvent(value){
	var request = new XMLHttpRequest();
	request.onreadystatechange = function(){
		if(this.readyState === 4){
			if(this.status === 200){
				if(this.responseText !== null)
				{
				try{
				var json_data = this.responseText;
				var json_obj = JSON.parse(json_data);
				if(json_obj.hasOwnProperty("authKey"))
				{
				pubnub.setAuthKey(json_obj.authKey);
				pubnub.setCipherKey(json_obj.cipherKey);
				console("Auth Kye set! " + this.responseText);
				}
				}
				}
			}
		}
	};
	request.open("POST", "status="+value, true);
	request.send(null);
}

function handleClick(cb){
	if(cb.checked)
	{
		value = "ON";
	}
	else
	{
		value = "OFF";
	}
	sendEvent(cb.id + "-" + value);
}

pubnub = new PubNub({
        publishKey : "pub-c-2bdeaffe-3be4-4af2-9b37-1b2e73389ef6",
        subscribeKey : "sub-c-a673c30e-2430-11eb-af2a-72ba4a3d8762",
        uuid: "76bc82e0-37db-11eb-adc1-0242ac120002"
    });

pubnub.addListener({
        status: function(statusEvent) {
            if (statusEvent.category === "PNConnectedCategory") {
                console.log("Connected to PubNub");
            }
        },
        message: function(msg) {
            console.log(msg.message.title);
            console.log(msg.message.description);
        },
        presence: function(presenceEvent) {
            // This is where you handle presence. Not important for now :)
        }
    })

pubnub.subscribe({
        channels: [myChannel]
    });

function publishUpdate(data, channel){
    pubnub.publish({
        channel: channel,
        message: data
        },
        function(status, response){
            if(status.error){
                console.log(status)
            }
            else{
                console.log("Message published with timetoken", response.timetoken)
                }
            }
        );

        function logout(){
        console.log("Logging out and unsubscribing");
        pubnub.unsubscribe({
        channels: [myChannels]
        });
        location.replace("/logout")


        }
}
