
const random = Math.ceil(Math.random() * 100)
const room_code_form = document.getElementById("room_code_form")
let hostname = window.location.hostname;

let room_code = null
room_code_form.addEventListener("submit", e => {
    e.preventDefault()
    console.log("Submitted Room Code");
    
    const formData = new FormData(room_code_form)
    const formValues = Object.fromEntries(formData.entries());
    room_code = formValues.code
    if (room_code) {
        const ws = new WebSocket(`ws://${hostname}:8000/room/ws/${random}/${room_code}`)

        ws.onmessage = function (event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        }
        var input = document.getElementById("text")
        function sendMessage() {
            ws.send(input.value)
            input.value = ''
        }
        const form = document.getElementById("chat")

        form.addEventListener("submit", e => {
            e.preventDefault()
            console.log(`Sending message ${input.value}`);
            sendMessage()
        })
    } else {
        alert("No room code provided")
    }
})


