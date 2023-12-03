//team_section.js

// Function to suggest team name
function suggestTeamName(teamNumber) {
    const inputElement = document.getElementById(`team${teamNumber}_name`);
    const teamName = inputElement.value;

    $.ajax({
        url: '/suggest_team',
        method: 'POST',
        data: { team_name: teamName },
        success: function (response) {
            const datalist = document.getElementById(`team${teamNumber}_suggestions`);
            datalist.innerHTML = '';

            response.forEach(function (name) {
                const option = document.createElement('option');
                option.value = name;
                datalist.appendChild(option);
            });

            const selectedTeamName = inputElement.value;

            $.ajax({
                url: '/get_team_data',
                method: 'POST',
                data: { team_name: selectedTeamName },
                success: function (teamData) {
                    const positionDropdown = document.getElementById(`team${teamNumber}_position`);
                    const pointsInput = document.getElementById(`team${teamNumber}_points`);
                    positionDropdown.value = teamData.position;
                    pointsInput.value = teamData.points;
                    updateAllTeamsTotalPoints();
                }
            });
        }
    });
}

// Function to calculate team points based on team position
function calculateTeamPoints(teamPosition) {
    if (teamPosition === "Group Stage") {
        return 0;
    } else if (teamPosition === "Semi-final") {
        return 100;
    } else if (teamPosition === "Runner-up") {
        return 400;
    } else if (teamPosition === "Champion") {
        return 600;
    }
    return 0;
}

// Function to update team points based on team position
function updateTeamPoints(teamNumber) {
    const positionDropdown = document.getElementById(`team${teamNumber}_position`);
    const pointsInput = document.getElementById(`team${teamNumber}_points`);
    const teamPosition = positionDropdown.value;
    const teamPoints = calculateTeamPoints(teamPosition);
    pointsInput.value = teamPoints;

    updateAllTeamsTotalPoints();
}

// Function to confirm team and insert data into the server
function confirmTeam(teamNumber) {
    const teamName = document.getElementById(`team${teamNumber}_name`).value;
    const teamPosition = document.getElementById(`team${teamNumber}_position`).value;
    const teamPoints = document.getElementById(`team${teamNumber}_points`).value;
    const user_id = "{{ session.get('user_id') }}";
    const data = {
        user_id: user_id,
        teamNumber: teamNumber,
        teamName: teamName,
        teamPosition: teamPosition,
        teamPoints: teamPoints
    };
    const confirmButton = document.getElementById(`confirm-button-${teamNumber}`);
    confirmButton.disabled = true; 
    confirmButton.textContent = 'Team Confirmed'; 

    $.ajax({
        url: '/insert_team_data',
        method: 'POST',
        data: data,
        success: function (response) {
            updateAllTeamsTotalPoints();
        }
    });
}

// Function to update the total points for all teams
function updateAllTeamsTotalPoints() {
    const team1Points = parseInt(document.getElementById('team1_points').value) || 0;
    const team2Points = parseInt(document.getElementById('team2_points').value) || 0;
    const allTeamsTotalPoints = team1Points + team2Points;

    const allTeamsTotalPointsDiv = document.getElementById('all-teams-total-points');
    allTeamsTotalPointsDiv.innerHTML = `All Teams Total Points: ${allTeamsTotalPoints}`;

    const user_id = "{{ session.get('user_id') }}";
    $.ajax({
        url: '/update_all_teams_total_points',
        method: 'POST',
        data: {
            user_id: user_id,
            all_teams_total_points: allTeamsTotalPoints
        },
        success: function (response) {

        }
    });
}

// Function to calculate combined total points
function calculateCombinedTotalPoints() {
    $.ajax({
        url: '/calculate_combined_total_points',
        method: 'POST',
        data: { user_id: '{{ session.get("user_id") }}' },
        success: function (response) {
            const totalPoints = response.total_points;
            const allPlayersTotalPoints = response.all_players_total_points;
            const allTeamsTotalPoints = response.all_teams_total_points;

            document.getElementById('total-points-display').innerHTML = `Total Points: ${totalPoints}`;
            document.getElementById('all-players-total-points-display').innerHTML = `All Players Total Points: ${allPlayersTotalPoints}`;
            document.getElementById('all-teams-total-points-display').innerHTML = `All Teams Total Points: ${allTeamsTotalPoints}`;
 
            document.getElementById('total-points-display').style.display = 'block';
            document.getElementById('all-players-total-points-display').style.display = 'block';
            document.getElementById('all-teams-total-points-display').style.display = 'block';
        }
    });
}

// Add these functions to fetch and update leaderboard
function fetchLeaderboard() {
    $.ajax({
        url: '/get_leaderboard',
        method: 'GET',
        success: function (leaderboardData) {
            updateLeaderboard(leaderboardData);
        }
    });
}

function updateLeaderboard(leaderboardData) {
    const leaderboardBody = $('#leaderboard-body');
    leaderboardBody.empty();

    leaderboardData.forEach(function (user) {
        const row = `<tr>
            <td>${user.user_name}</td>
            <td>${user.combined_total_points}</td>
        </tr>`;
        leaderboardBody.append(row);
    });
}

// Add these functions to fetch and update top players
function fetchTopPlayers() {
    $.ajax({
        url: '/get_top_players',
        method: 'GET',
        success: function (topPlayersData) {
            updateTopPlayers(topPlayersData);
        }
    });
}

function updateTopPlayers(topPlayersData) {
    const topPlayersBody = $('#top-players-body');
    topPlayersBody.empty();

    topPlayersData.forEach(function (player) {
        const row = `<tr>
            <td>${player.player_name}</td>
            <td>${player.role}</td>
            <td>${player.player_total_points}</td>
        </tr>`;
        topPlayersBody.append(row);
    });
}

// Fetch and update leaderboard
fetchLeaderboard();

// Fetch and update top players
fetchTopPlayers();
