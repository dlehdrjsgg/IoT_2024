var url = 'http://127.0.0.1:5000/api/get-item-details';
var requestData = {
    category: 'groceries',
    store_id: 'S123',
};

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestData)
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
})
.then(responseData => {
    const itemList = document.getElementById('Deadlined-item-list');

    // 현재 날짜와 7일 후 날짜를 계산
    const currentDate = new Date();
    const oneWeekLater = new Date();
    oneWeekLater.setDate(currentDate.getDate() + 7); // 현재 날짜에 7일을 더합니다.

    // 데이터 필터링
// 먼저 item들을 저장할 배열을 생성
const itemsToDisplay = responseData.items.map(item => {
    const deadlineDate = new Date(item.deadline);
    const leftDays = Math.floor((deadlineDate - currentDate) / (1000 * 60 * 60 * 24));


    if (deadlineDate <= oneWeekLater) {
        return {
            productName: item.productName,
            leftDays: leftDays,
            deadline: item.deadline,
            time: item.time,
            barcode: item.barcode
        };
    }
}).filter(item => item !== undefined); 


itemsToDisplay.sort((a, b) => a.leftDays - b.leftDays);

    itemsToDisplay.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item.productName} : ${item.leftDays}일 남음 (유통기한: ${item.deadline}, 등록일: ${item.time}, 바코드: ${item.barcode})`;
        itemList.appendChild(listItem);
    });
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});