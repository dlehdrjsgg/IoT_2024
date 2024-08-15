var url = 'http://192.168.215.2:5000/api/get-item-details';
var url2 = 'http://192.168.215.2:5000/api/remove-item';
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
    const itemList = document.getElementById('item-list');

    responseData.items.forEach(item => {
        const listItem = document.createElement('li');
        listItem.textContent = `${item.productName} (Expiry: ${item.deadline}, Registered: ${item.time}, Barcode: ${item.barcode})`;

        const deleteButton = document.createElement('button');
        deleteButton.textContent = '삭제';
        deleteButton.classList.add('delete-btn');

        deleteButton.addEventListener('click', function() {
            listItem.remove();
            fetch(url2, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ barcode: item.barcode, time: item.time })
            })
        });

        listItem.appendChild(deleteButton);
        itemList.appendChild(listItem);
    });
})
.catch(error => {
    console.error('There was a problem with the fetch operation:', error);
});