// Variable to store the currently selected row for editing
let selectedRow = null;

// Function to enable editing of the table cell on focus
function enableEditing(event) {
    let target = event.target;
    target.focus();
    target.setAttribute('contenteditable', 'true');

    if (!selectedRow) {
        selectedRow = target.parentElement;
    }
}

// Function to save the changes after editing a table cell
function saveChanges() {
    if (selectedRow) {
        updateRecord(selectedRow);
        selectedRow = null;
    }
}

// Function to send an update request for a record
function updateRecord(row) {
    // Collect the updated data from the table row
    let recordId = row.querySelector('.record-id').value;
    let first_name = row.children[0].innerText;
    let last_name = row.children[1].innerText;
    let card_number = row.children[2].innerText;
    let phone_number = row.children[3].innerText;
    let bonus_points = row.children[4].innerText;
    let birthdate = row.children[5].innerText;

    let data = {
        id: recordId,
        first_name: first_name,
        last_name: last_name,
        phone_number: phone_number,
        card_number: card_number,
        bonus_points: bonus_points,
        birthdate: birthdate
    };
    
    // Send the updated data to the server
    fetch('/update_record', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(json => {
            if (json.status === 'success') {
                alert('Record updated successfully');
                setTimeout(() => {
                    refreshTableData(); // Refresh table data after a successful update
                }, 500); // Add a 500ms delay
            } else {
                alert('Error: ' + json.message);
            }
        })
    }


// Add this new function to handle search
function search() {
    const searchType = document.getElementById('search_type').value;
    const searchQuery = document.getElementById('search_query').value;

    fetch(`/search?search_type=${searchType}&search_query=${searchQuery}`)
        .then(response => response.json())
        .then(json => {
            if (json.status === 'error') {
                alert('Error: ' + json.message);
            } else {
                displayResults(json);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while searching');
        });
}

// Modify the 'DOMContentLoaded' event in your scripts.js
document.addEventListener('DOMContentLoaded', function () {
    refreshTableData(); // Refresh table data when the page is loaded
    document.getElementById('search_button').addEventListener('click', search); // Add this line to attach the event listener to the search button
    document.getElementById('refresh_button').addEventListener('click', refreshTableData);
});
   
    // Refresh table data when the page is loaded
document.addEventListener('DOMContentLoaded', function () {
    refreshTableData();
    });

    // Function to display the fetched data in the table
    function displayResults(data) {
        let tableBody = document.querySelector('.my-table tbody');
        tableBody.innerHTML = '';
        
        // Create table rows and cells for each record
        data.forEach(record => {
            let row = document.createElement('tr');
            
            // Create and append each cell to the row
            let firstNameCell = document.createElement('td');
            firstNameCell.innerText = record.first_name;
            firstNameCell.contentEditable = 'true';
            firstNameCell.addEventListener('focus', enableEditing);
            row.appendChild(firstNameCell);
    
            let lastNameCell = document.createElement('td');
            lastNameCell.innerText = record.last_name;
            lastNameCell.contentEditable = 'true';
            lastNameCell.addEventListener('focus', enableEditing);
            row.appendChild(lastNameCell);
    
            let cardNumberCell = document.createElement('td');
            cardNumberCell.innerText = record.card_number;
            cardNumberCell.contentEditable = 'true';
            cardNumberCell.addEventListener('focus', enableEditing);
            row.appendChild(cardNumberCell);
    
            let phoneNumberCell = document.createElement('td');
            phoneNumberCell.innerText = record.phone_number;
            phoneNumberCell.contentEditable = 'true';
            phoneNumberCell.addEventListener('focus', enableEditing);
            row.appendChild(phoneNumberCell);
    
            let bonusPointsCell = document.createElement('td');
            bonusPointsCell.innerText = record.bonus_points;
            bonusPointsCell.contentEditable = 'true';
            bonusPointsCell.addEventListener('focus', enableEditing);
            row.appendChild(bonusPointsCell);

            let birthdateCell = document.createElement('td');
            birthdateCell.innerText = record.birthdate;
            birthdateCell.contentEditable = 'true';
            birthdateCell.addEventListener('focus', enableEditing);
            row.appendChild(birthdateCell);
        
            let recordIdInput = document.createElement('input');
            recordIdInput.type = 'hidden';
            recordIdInput.classList.add('record-id');
            recordIdInput.value = record.id;
            row.appendChild(recordIdInput);
            
            // Append the row to the table body
            tableBody.appendChild(row);
        });
    }        
    
    // Function to fetch and display the table data
    function refreshTableData() {
        fetch('/get_table_data')
            .then(response => response.json())
            .then(json => {
                // Use the displayResults function to populate the table with the fetched data
                console.log('Fetched data:', json);
                displayResults(json);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while fetching table data');
            });
    }

    // Function to handle key press events in editable table cells
    function handleKeyPress(event, target) {
        if (event.keyCode === 13) { // Check if the pressed key is Enter (keyCode 13)
            event.preventDefault(); // Prevent the default action
            target.blur(); // Remove focus from the cell
        }
    }
    