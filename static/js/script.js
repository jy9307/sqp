let questions = [];
document.getElementById('send_btn').addEventListener('click', function() {
    const input = document.getElementById('messageInput');
    const message = input.value;
    input.value = '';
    sendQuestion(message);
});

function displayData(data) {
    const div = document.getElementById('QFeed');
    let feedback = data
    feedback = feedback
                    .replace(/\n/g, '<br>')
                    .replace(/\*/g, '')  // \n을 <br>로 변경;
    div.innerHTML = '';
    div.innerHTML = feedback;
}


async function sendQuestion(message) {

    questions.push(message)
    try{
        const response = await fetch('http://127.0.0.1:5000/query', {
            method : 'POST',
            headers : {
                'Content-Type' : 'application/json'
            },
            body : JSON.stringify({question : questions })
        });

        if (!response.ok) {
            throw new Error('Request failed with status ' + response.status);
        }

        const data = await response.json() ;
        displayData(data.response)

    } catch (error) {
        console.error('문제발생 : ',error);
    }
}