function addRow(tableId) {
    const tbody = document.getElementById(tableId).querySelector('tbody');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td></td>
        <td><input type="number" step="any" name="${tableId === 'stocks' ? 'stocks_lengths' : 'cuts_lengths'}" placeholder="Enter length" min="0" required /></td>
        <td><input type="number" name="${tableId === 'stocks' ? 'stocks_quantities' : 'cuts_quantities'}" placeholder="Enter quantity" min="0" /></td>
        ${tableId === 'cuts' ? `
            <td>
                <input type="number" step="any" name="cuts_left_wall_angles" placeholder="Left" min="0" max="180"/>
                <input type="number" step="any" name="cuts_right_wall_angles" placeholder="Right" min="0" max="180"/>
            </td>` : ''}
        <td><button type="button" class="delete-button" onclick="deleteRow(this)">X</button></td>
    `;
    tbody.appendChild(newRow);

    // Re-number all rows
    Array.from(tbody.rows).forEach((row, index) => {
        row.cells[0].innerText = index + 1;
    });
}

function deleteRow(button) {
    // Get the tbody element from the button's context before removing the row
    const tbody = button.closest('tbody');
    const row = button.closest('tr');
    row.remove();

    // re-number the remaining rows
    Array.from(tbody.rows).forEach((row, index) => {
        row.cells[0].innerText = index + 1;
    });
}
// Assign empty values to 0 in order to keep valid input type restrictions and reassign values server-side
document.querySelector("form").addEventListener("submit", function (event) {
    const kerfInput = document.getElementById("kerf");
    const depthInput = document.getElementById("depth");
    const stocksQuantitiesInputs = document.getElementsByName("stocks_quantities");
    const cutsQuantitiesInputs = document.getElementsByName("cuts_quantities");
    const cutsLeftWallAnglesInputs = document.getElementsByName("cuts_left_wall_angles");
    const cutsRightWallAnglesInputs = document.getElementsByName("cuts_right_wall_angles");

    if (kerfInput.value.trim() === "") {
        kerfInput.value = 0;
    }
    if (depthInput.value.trim() === "") {
        depthInput.value = 0;
    }
    stocksQuantitiesInputs.forEach(input => {
        if (input.value.trim() === "") {
            input.value = 0;
        }
    });
    // Assign empty to 1 assuming any cut length will have at least one cut
    cutsQuantitiesInputs.forEach(input => {
        if (input.value.trim() === "") {
            input.value = 1;
        }
    });            
    cutsLeftWallAnglesInputs.forEach(input => {
        if (input.value.trim() === "") {
            input.value = 0;
        }
    });
    cutsRightWallAnglesInputs.forEach(input => {
        if (input.value.trim() === "") {
            input.value = 0;
        }
    });
});