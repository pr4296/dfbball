<template>
    <div class="card"><h2>Box Score</h2>
        <table>
            <thead>
                <th>Opponent</th>
                <th>Game Date</th>
                <th>PTS</th>
                <th>REB</th>
                <th>AST</th>
                <th>STL</th>
                <th>BLK</th>
                <th>3PM</th>
                <th>TOV</th>
            </thead>
            <tbody>
                <tr v-for="row in this.boxStats" :key="row.gameId"
                    @click="goToGame(row.gameId)">
                    <td>{{ row.atOrVs }}{{ row.opposingTeamAbbreviation }}</td>
                    <td>{{ getLocalGameTime(row.startTime) }}</td>
                    <td>{{ row.pts }}</td>
                    <td>{{ parseInt(row.offReb)+parseInt(row.defReb) }}</td>
                    <td>{{ row.ast }}</td>
                    <td>{{ row.stl }}</td>
                    <td>{{ row.blk }}</td>
                    <td>{{ row.fg3PtMade }}</td>
                    <td>{{ row.tov }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PlayerBoxScore",
    computed: {
        boxStats: function() {
            console.log('boxstats');
            console.log(store.state.apiDataPlayerBoxStats);
            return store.state.apiDataPlayerBoxStats;
        }
    },
    methods: {
        fetchPlayerBoxStats: function() {
            console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerBoxStats.php?id='+this.$route.params.id;
            console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    // console.log(responseData);
                    for (var i in responseData) {
                        var row = responseData[i];
                        row['startTime'] = row['startTime'].substring(0, 10);
                        var isHome = row['abbreviation'] == row['homeTeamAbbreviation'];
                        row['opposingTeamAbbreviation'] = isHome ? row['awayTeamAbbreviation'] : row['homeTeamAbbreviation'];
                        row['atOrVs'] = isHome ? 'vs' : '@';
                    }
                    store.commit('setApiDataPlayerBoxStats', responseData);
            });
        },
        goToGame: function(gameId) {
            router.push('/game/'+gameId)
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        getLocalGameTime: function(date) {
            var utcDatePlusOffset = new Date(date);
            var offset = utcDatePlusOffset.getTimezoneOffset();
            var localDate = new Date(utcDatePlusOffset-offset*60*1000);
            // return localDate;

            var now = new Date();
            var currDateUTC = new Date(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate());
            var gameDateUTC = new Date(localDate.getUTCFullYear(), localDate.getUTCMonth(), localDate.getUTCDate());

            if (currDateUTC == gameDateUTC) return "Today";
            if (currDateUTC - gameDateUTC < 24*60*60*1000 && currDateUTC > gameDateUTC) return "Yesterday ";
            if (currDateUTC - gameDateUTC > -24*60*60*1000 && currDateUTC < gameDateUTC) return "Tomorrow ";
            // console.log('at end');

            var days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
            var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

            
            localDate = days[localDate.getDay()]+", "+months[localDate.getMonth()]+" "+localDate.getDate()+", "+localDate.getFullYear();
            return localDate;
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchPlayerBoxStats();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchPlayerBoxStats();
        }
    },
    created() {
        this.fetchPlayerBoxStats();
    }
};
</script>