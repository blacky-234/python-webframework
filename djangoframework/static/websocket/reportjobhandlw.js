
// let ws = new WebSocket("ws://127.0.0.1:8000/ws/echo");

// ws.onopen = () => {
//     console.log("WebSocket connected");
//     ws.send("hello");   // send only after connection is open
// };

// ws.onmessage = (e) => {
//     console.log("Received:", e.data);
// };

// ws.onerror = (e) => {
//     console.error("WebSocket error:", e);
// };

// ws.onclose = () => {
//     console.log("WebSocket closed");
// };

//TODO: Working good
// $('#job-create-btn').on('click',function(){
//     console.log("create button clicked");
//     $.get('start/',function(data,status,xhr){
//         console.log("cretae console : ",data);
//         console.log("status : ",status);
//     }).fail(function(xhr, status, error) {
//             console.error("Error:", error);
//     });
// })  


$('#job-create-btn').on('click',function(){
    console.log("create button clicked");
   fetch('start/').then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok " + response.statusText);
        }
        return response.json();
    }).then(data => {
        $('#report-table-body').append(data.html);
        connectProgressSocket(data.job_id);
    }).catch(error => {
        console.error("Error:", error);
    });
}) 


function connectProgressSocket(jobId) {

    const ws = new WebSocket(
        `ws://${window.location.host}/progr/${jobId}/`
    );

    ws.onmessage = function (e) {
        const data = JSON.parse(e.data);

        console.log("Progress:", data.progress);

        // 3️⃣ Update UI live
        $(`#progress-${jobId}`).text(data.progress + "%");

        if (data.progress >= 100) {
            ws.close();
        }
    };

    ws.onclose = () => console.log("WebSocket closed for", jobId);
}
