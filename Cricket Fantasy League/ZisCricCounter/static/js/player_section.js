// player_section.js
let playerCounter = 0;

// Function to add a new player input row
function addPlayer() {
        if (playerCounter < 13) {
            playerCounter++;
            const totalPointsDiv = `<div id="totalPoints${playerCounter}" class="total-points"></div>`;
            const newRow = `<div class="player-row">
                <h3 class= "player-number-h3" onclick="togglePlayerInnings(${playerCounter})">Player ${playerCounter}</h3>

                <input type="text" list="playerSuggestions" class= "player-name-input" name="player_name" id="player_name${playerCounter}" placeholder="Player Name" onkeyup="suggestPlayer(this)" required>
                <datalist id="playerSuggestions"></datalist>

                <select  class= "payer-role-dropdown-menu" name="player_role" id="player_role${playerCounter}" required>
                    <option value="Batsman">Batsman</option>
                    <option value="Bowler">Bowler</option>
                    <option value="All-Rounder">All-Rounder</option>
                </select>

                <button type="button" class="add-inning" onclick="addInning(${playerCounter})">Add Inning</button>
                <button type="button" class="toggle-button" id="toggleButton${playerCounter}" onclick="togglePlayerInnings(${playerCounter}, this)">Collapse</button>
		<br> <br>
                <div class= "player-total-points" id="totalPoints${playerCounter}"></div>

                <div id="player${playerCounter}"></div>

            </div>`;

            $('#player-section').append(newRow);


            if (playerCounter === 13) {
                const lineBreak = '<br>';
                const calculateAllPlayersTotalPointsButton = `<button type="button" class="calculate-all-players-total-points-button" onclick="calculateAllPlayersTotalPoints()">Calculate All Players Total Points</button>`;

                $('#player-section').append(lineBreak);
                $('#player-section').append(lineBreak);
                $('#player-section').append(calculateAllPlayersTotalPointsButton);
            }
        } else {
            alert("Maximum limit of players reached.");
        }
    }

// Function to suggest player name
function suggestPlayer(inputElement) {
    const playerName = inputElement.value;

    $.ajax({
        url: '/suggest_player',
        data: { query: playerName },
        success: function (response) {
            const datalist = document.getElementById('playerSuggestions');
            datalist.innerHTML = '';

            response.forEach(function (name) {
                const option = document.createElement('option');
                option.value = name;
                datalist.appendChild(option);
            });
        }
    });


    inputElement.addEventListener('change', function (event) {
        const selectedPlayer = event.target.value;

        $.ajax({
            url: '/get_player_role',
            data: { player_name: selectedPlayer },
            success: function (role) {
                const playerId = inputElement.id.match(/\d+/)[0];
                const roleDropdown = $(`#player_role${playerId}`);
                roleDropdown.val(role);
                roleDropdown.change();

                fetchPlayerInningsInfo(selectedPlayer, role, playerId);

            }
        });
    });
}



// Function to fetch and update player innings info
function fetchPlayerInningsInfo(playerName, role, playerId) {
    $.ajax({
        url: '/fetch_player_innings_info',
        data: { player_name: playerName, role: role },
        success: function (inningsInfo) {
            console.log('Innings Info:', inningsInfo); 

            updatePlayerInningsInfo(playerId, inningsInfo, playerName);
        }
    });
}




// Function to update player innings info in the UI
function updatePlayerInningsInfo(playerId, inningsInfo, playerName) {
    console.log('Updating Player Innings Info:', inningsInfo); 

    $(`#player${playerId} .inning-row`).remove();

    inningsInfo.forEach(function (inning, index) {
        addInningRow(playerId, inning, index + 1, playerName);
    });


    updateTotalPointsDisplay(playerId);
}


// Function to add an inning row
function addInningRow(playerId, inning, inningNo, playerName) {
    let inningRow = `<div class="inning-row">
        <label class="inning-no-label">Inning #${inningNo}</label>`;

if (
    inning.hasOwnProperty(`inning_${inningNo}_runs`) &&
    inning.hasOwnProperty(`inning_${inningNo}_wickets`)
) {
    inningRow += `<input type="number" id="add-inning-runs-input-all-rounder" class="add-inning-runs-input-dy" name="inning${inningNo}_runs" placeholder="Runs" value="${inning[`inning_${inningNo}_runs`] || ''}" required>
        <input type="number" id="add-inning-strike-rate-input-al-rounder" class="add-inning-strike-rate-input-dy" name="inning${inningNo}_strike_rate" placeholder="Strike Rate" value="${inning[`inning_${inningNo}_strike_rate`] || ''}" required>
        <input type="number" id="add-inning-wickets-input-all-rounder" class="add-inning-wickets-input-dy" name="inning${inningNo}_wickets" placeholder="Wickets" value="${inning[`inning_${inningNo}_wickets`] || ''}" required>
        <input type="number" id="add-inning-economy-rate-input-all-rounder" class="add-inning-economy-rate-input-dy" name="inning${inningNo}_economy_rate" placeholder="Economy Rate" value="${inning[`inning_${inningNo}_economy_rate`] || ''}" required>`;
} else if (inning.hasOwnProperty(`inning_${inningNo}_runs`)) {
    inningRow += `<input type="number" class="add-inning-runs-input" style="margin-bottom:10px;" name="inning${inningNo}_runs" placeholder="Runs" value="${inning[`inning_${inningNo}_runs`] || ''}" required>
        <input type="number" class="add-inning-strike-rate-input" name="inning${inningNo}_strike_rate" placeholder="Strike Rate" value="${inning[`inning_${inningNo}_strike_rate`] || ''}" required>`;
} else if (inning.hasOwnProperty(`inning_${inningNo}_wickets`)) {
    inningRow += `<input type="number" class="add-inning-wickets-input" style="margin-bottom:10px;" name="inning${inningNo}_wickets" placeholder="Wickets" value="${inning[`inning_${inningNo}_wickets`] || ''}" required>
        <input type="number" class="add-inning-economy-rate-input" name="inning${inningNo}_economy_rate" placeholder="Economy Rate" value="${inning[`inning_${inningNo}_economy_rate`] || ''}" required>`;
}


    inningRow += `<input type="number" class="add-inning-points" name="inning${inningNo}_points" placeholder="Points" readonly>
        <button type="button" class="confirm-player-inning-button" data-inning="${inningNo}" onclick="confirmPlayerInning(${playerId}, ${inningNo}, '${playerName}')">Confirm</button>
   
 </div>`;

    const newInningRow = $(`#player${playerId}`).append(inningRow);

    newInningRow.find(`input[name^="inning"][name$="_runs"], input[name^="inning"][name$="_strike_rate"], input[name^="inning"][name$="_wickets"], input[name^="inning"][name$="_economy_rate"]`).on('input', function() {
        calculatePoints(playerId);
    });

    newInningRow.find(`input[name^="inning"][name$="_points"]`).on('input', function() {
        calculatePoints(playerId);
    });


    $(`#player${playerId} .calculate-player-total-points`).remove();

    const calculatePlayerTotalPointsButton = `<button type="button" class="calculate-player-total-points" onclick="insertPlayerTotalPoints(${playerId})">Calculate Player Total Points</button>`;

    $(`#player${playerId}`).append(calculatePlayerTotalPointsButton);

    const totalPointsElement = $(`#player${playerId}`).find('.total-points');
    if (totalPointsElement.length > 0) {
        totalPointsElement.remove();
    }

    $(`#player${playerId} .confirm-player-button`).remove();
    const confirmPlayerButton = `<button type="button" class="confirm-player-button" onclick="confirmPlayer(${playerId})">Confirm Player</button>`;
    $(`#player${playerId}`).append(confirmPlayerButton);
}



// Function to add an inning input row
function addInning(playerId) {
    const maxInnings = 11;
    const currentInnings = $(`#player${playerId} .inning-row`).length;
    const playerRole = $(`#player_role${playerId}`).val();
    const playerName = $(`#player_name${playerId}`).val();

    if (currentInnings < maxInnings) {
        const inningNo = currentInnings + 1;
        let inningRow = `<div class="inning-row">

            <label class= "inning-no-label">Inning #${inningNo}</label>`;

        if (playerRole === 'Batsman') {
            inningRow += `<input type="number" class= "add-inning-runs-input" name="inning${inningNo}_runs" placeholder="Runs" required>
                         <input type="number" class= "add-inning-strike-rate-input" name="inning${inningNo}_strike_rate" placeholder="Strike Rate" required>`;
        } else if (playerRole === 'Bowler') {
            inningRow += `<input type="number" class= "add-inning-wickets-input" name="inning${inningNo}_wickets" placeholder="Wickets" required>
                         <input type="number" class= "add-inning-economy-rate-input" name="inning${inningNo}_economy_rate" placeholder="Economy Rate" required>`;
        } else if (playerRole === 'All-Rounder') {
            inningRow += `<input type="number" id= "add-inning-runs-input-all-rounder" class= "add-inning-runs-input" name="inning${inningNo}_runs" placeholder="Runs" required>
                         <input type="number" id= "add-inning-strike-rate-input-al-rounder" class= "add-inning-strike-rate-input" name="inning${inningNo}_strike_rate" placeholder="Strike Rate" required>
                         <input type="number" id= "add-inning-wickets-input-all-rounder" class= "add-inning-wickets-input" name="inning${inningNo}_wickets" placeholder="Wickets" required>
                         <input type="number" id= "add-inning-economy-rate-input-all-rounder" class= "add-inning-economy-rate-input" name="inning${inningNo}_economy_rate" placeholder="Economy Rate" required>`;
        }

        inningRow += `<input type="number" class= "add-inning-points" name="inning${inningNo}_points" placeholder="Points" readonly>
                     <button type="button" class="confirm-player-inning-button" data-inning="${inningNo}"  onclick="confirmPlayerInning(${playerId}, ${inningNo}, '${playerName}')">Confirm</button>
			
                     </div>`;

        const newInningRow = $(`#player${playerId}`).append(inningRow);

        $(newInningRow).on('input', `input[type="number"]`, function() {
            calculatePoints(playerId);
        });



        $(`#player${playerId} .calculate-player-total-points`).remove();

	const lineBreak = '<br>';
        const calculatePlayerTotalPointsButton = `<button type="button" class="calculate-player-total-points" onclick="insertPlayerTotalPoints(${playerId})">Calculate Player Total Points</button>`;
	newInningRow.append(lineBreak);
        newInningRow.append(calculatePlayerTotalPointsButton);

        const totalPointsElement = $(`#player${playerId}`).find('.total-points');
        if (totalPointsElement.length > 0) {
	    totalPointsElement.remove();
        }

	$(`#player${playerId} .confirm-player-button`).remove();
	const confirmPlayerButton = `<button type="button" class= "confirm-player-button" onclick="confirmPlayer(${playerId})">Confirm Player</button>`;
	newInningRow.append(confirmPlayerButton);


    } else {
        alert("Maximum innings reached for this player.");
    }
}


// Function to calculate points
function calculatePoints(playerId) {
    $(`#player${playerId} .inning-row`).each(function(index, element) {
        const runs = parseFloat($(element).find('input[name^="inning"][name$="_runs"]').val()) || 0;
        const strikeRate = parseFloat($(element).find('input[name^="inning"][name$="_strike_rate"]').val()) || 0;
        const wickets = parseFloat($(element).find('input[name^="inning"][name$="_wickets"]').val()) || 0;
        const economyRate = parseFloat($(element).find('input[name^="inning"][name$="_economy_rate"]').val()) || 0;
        const role = $(`#player_role${playerId}`).val();
        const pointsInput = $(element).find('input[name^="inning"][name$="_points"]');

        let points = 0;

        if (role === 'Batsman') {
            if (strikeRate > 100) {
                points = runs * 1.5;
            } else if (strikeRate >= 80 && strikeRate <= 100) {
                points = runs * 1;
            } else {
                points = runs * 0.8;
            }
        } else if (role === 'Bowler') {
            if (economyRate < 5) {
                points = wickets * 12;
            } else if (economyRate >= 5 && economyRate <= 6.5) {
                points = wickets * 10;
            } else {
                points = wickets * 8;
            }
        } else if (role === 'All-Rounder') {
            const battingPoints = (strikeRate > 100) ? runs * 1.5 : (strikeRate >= 80) ? runs * 1 : runs * 0.8;
            const bowlingPoints = (economyRate < 5) ? wickets * 12 : (economyRate <= 6.5) ? wickets * 10 : wickets * 8;
            points = battingPoints + bowlingPoints;
        }

        pointsInput.val(points.toFixed(2));


    });
}


// Function to confirm player inning
function confirmPlayerInning(playerId, inningNo, playerName) {
    const confirmButton = $(`#player${playerId} .inning-row:nth-of-type(${inningNo}) .confirm-player-inning-button`);
    confirmButton.prop('disabled', true);
    confirmButton.text('Confirmed');

    const runs = parseInt($(`#player${playerId} .inning-row:nth-of-type(${inningNo}) input[name^="inning"][name$="_runs"]`).val()) || 0;
    const strikeRate = parseFloat($(`#player${playerId} .inning-row:nth-of-type(${inningNo}) input[name^="inning"][name$="_strike_rate"]`).val()) || 0;
    const wickets = parseInt($(`#player${playerId} .inning-row:nth-of-type(${inningNo}) input[name^="inning"][name$="_wickets"]`).val()) || 0;
    const economyRate = parseFloat($(`#player${playerId} .inning-row:nth-of-type(${inningNo}) input[name^="inning"][name$="_economy_rate"]`).val()) || 0;
    const points = parseFloat($(`#player${playerId} .inning-row:nth-of-type(${inningNo}) input[name^="inning"][name$="_points"]`).val()) || 0;

    insertInningData(playerName, playerId, inningNo, runs, strikeRate, wickets, economyRate, points);
}


// Function to insert inning data
function insertInningData(playerName, playerId, inningNo, runs, strikeRate, wickets, economyRate, points) {
    const role = $(`#player_role${playerId}`).val();

$.ajax({
    url: '/insert_inning_data',
    method: 'POST',
    data: {
        player_name: playerName,
        inning_no: inningNo,
        playerId: playerId,
        runs: runs,
        strike_rate: strikeRate,
        wickets: wickets,
        economy_rate: economyRate,
        points: points, // Add the 'points' data
        role: role,
    },
    success: function (response) {


    }
});

}


// Function to calculate player total points
function calculatePlayerTotalPoints(playerId) {
    const role = $(`#player_role${playerId}`).val();
    const playerName = $(`#player_name${playerId}`).val();
    let totalPoints = 0;

    $(`#player${playerId} .inning-row`).each(function(index, element) {
        calculatePoints(playerId, index + 1);
        const pointsInput = $(element).find('input[name^="inning"][name$="_points"]');
        const inningPoints = parseFloat(pointsInput.val()) || 0;
        totalPoints += inningPoints;
    });

    return totalPoints; 

}


// Function to insert player total points
function insertPlayerTotalPoints(playerId) {
    const role = $(`#player_role${playerId}`).val();
    const playerName = $(`#player_name${playerId}`).val();
    let totalPoints = 0;

    $(`#player${playerId} .inning-row`).each(function (index, element) {
        calculatePoints(playerId, index + 1);
        const pointsInput = $(element).find('input[name^="inning"][name$="_points"]');
        const inningPoints = parseFloat(pointsInput.val()) || 0;
        totalPoints += inningPoints;
    });

    const totalPointsElement = $(`#player${playerId}`).find('.total-points');
    if (totalPointsElement.length === 0) {

        $(`#player${playerId} .total-points`).remove();

        const totalPointsDisplay = `<div style= "margin-left: 30px;" class="total-points">Total Points: ${totalPoints.toFixed(2)}, Role: ${role}</div>`;
        $(`#player${playerId}`).append(totalPointsDisplay);

    } else {

        $(`#player${playerId} .total-points`).remove();
        totalPointsElement.html(`Total Points: ${totalPoints}, Role: ${role}`);
    }

    $.ajax({
        url: '/insert_player_total_points',
        method: 'POST',
        data: {
            player_name: playerName,
            role: role,
            total_points: totalPoints,
        },
        success: function (response) {
            // Handle success if needed
        }
    });
}


// Function to confirm player
function confirmPlayer(playerId) {
    const playerName = $(`#player_name${playerId}`).val();
    const playerRole = $(`#player_role${playerId}`).val();
    const totalPoints = calculatePlayerTotalPoints(playerId); 

    const confirmPlayerButton = $(`#player${playerId} .confirm-player-button`);
    confirmPlayerButton.prop('disabled', true);
    confirmPlayerButton.text('Player Confirmed');
  
    $.ajax({
        url: '/insert_player_data',
        method: 'POST',
        data: {
            player_id: playerId,
            player_name: playerName,
            player_role: playerRole,
            player_total_points: totalPoints,
        },
        success: function (response) {
            if (response.success) {
                alert(`Player ${playerId} confirmed and data inserted.`);
            } else {
                alert(`Failed to confirm player.`);
            }
        }
    });
}


// Function to calculate all players' total points
function calculateAllPlayersTotalPoints() {

    $.ajax({
        url: '/calculate_all_players_total_points', 
        method: 'POST', 
        success: function (response) {
            if (response.success) {
                alert("All players' total points calculated and updated.");

                const allPlayerTotalPointsDiv = document.getElementById('all-player-total-points');
		const allBatsmanTotalPointsDiv = document.getElementById('all-batsman-total-points');
		const allBowlerTotalPointsDiv = document.getElementById('all-bowler-total-points');
		const allAllronderTotalPointsDiv = document.getElementById('all-allrounder-total-points');

                allPlayerTotalPointsDiv.innerHTML = `All Player Total Points: ${response.total_points}`;

                allBatsmanTotalPointsDiv.innerHTML = `All Batsman Total Points: ${response.total_batsman_points}`;

                allBowlerTotalPointsDiv.innerHTML = `All Bowler Total Points: ${response.total_bowler_points}`;

                allAllronderTotalPointsDiv.innerHTML = `All All-rounder Total Points: ${response.total_all_rounder_points}`;

            } else {
                alert("Failed to calculate all players' total points.");
            }
        }
    });
}

 
// Function to toggle the visibility of player innings list and total points
function togglePlayerInnings(playerId, buttonElement) {
    const playerInningsList = $(`#player${playerId}`);
    const toggleButton = $(`#toggleButton${playerId}`);
    const totalPointsDiv = $(`#totalPoints${playerId}`);

    if (playerInningsList.is(':visible')) {
        playerInningsList.hide();
        totalPointsDiv.show();
        $(buttonElement).text('Expand');
        toggleButton.text('Expand');
    } else {
        playerInningsList.show();
        totalPointsDiv.hide(); 
        $(buttonElement).text('Collapse');
        toggleButton.text('Collapse');
    }

    updateTotalPointsDisplay(playerId);
}


// Function to update the total points display
function updateTotalPointsDisplay(playerId) {
    const totalPoints = calculatePlayerTotalPoints(playerId);
    const totalPointsDiv = $(`#totalPoints${playerId}`);
    totalPointsDiv.html(`Total Points: ${totalPoints.toFixed(2)}`);
}

updateTotalPointsDisplay(playerCounter);
