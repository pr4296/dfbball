<template>
    <div class="card"><h2>Box Score</h2>
        <table>
            <thead>
                <th>W/L</th>
                <th>OPP</th>
                <th>Date</th>
                <th>PTS</th>
                <th>REB</th>
                <th>AST</th>
                <th>STL</th>
                <th>BLK</th>
                <th>FG</th>
                <th>3PT</th>
                <th>FT</th>
                <th>TOV</th>
                <th>FLS</th>
                <th>+/-</th>
                <th>MIN</th>
            </thead>
            <tbody>
                <tr v-for="row in this.boxStats" :key="row.gameId"
                    @click="goToGame(row.gameId)">
                    <td><span :class="[wonGame(row.awayScoreTotal, row.homeScoreTotal, row.awayTeamId, row.homeTeamId, row.playerTeamId) ? 'boxscore-win' : 'boxscore-loss' ]">
                        {{ wonGame(row.awayScoreTotal, row.homeScoreTotal, row.awayTeamId, row.homeTeamId, row.playerTeamId) ? 'W' : 'L' }}
                        </span>
                    </td>
                    <td>{{ row.atOrVs }}{{ row.opposingTeamAbbreviation }}</td>
                    <td style="font-size: 12px">{{ getLocalGameTime(row.startTime) }}</td>
                    <td>{{ row.pts }}</td>
                    <td>{{ parseInt(row.offReb)+parseInt(row.defReb) }}</td>
                    <td>{{ row.ast }}</td>
                    <td>{{ row.stl }}</td>
                    <td>{{ row.blk }}</td>
                    <td>{{ parseInt(row.fg2PtMade)+parseInt(row.fg3PtMade) }}/{{ parseInt(row.fg2PtAtt)+parseInt(row.fg3PtAtt) }}</td>
                    <td>{{ row.fg3PtMade }}/{{ row.fg3PtAtt }}</td>
                    <td>{{ row.ftMade }}/{{ row.ftAtt }}</td>
                    <td>{{ row.tov }}</td>
                    <td>{{ row.foulPers }}</td>
                    <td>{{ row.plusMinus }}</td>
                    <td>{{ Math.ceil(row.minSeconds/60) }}</td>
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

            localDate = (localDate.getMonth()+1)+'/'+(localDate.getDate())+'/'+(localDate.getYear()%100);
            return localDate;
        },
        wonGame: function(awayScore, homeScore, awayId, homeId, currTeamId) {
            return (parseInt(awayScore) > parseInt(homeScore) && awayId == currTeamId) || (parseInt(awayScore) < parseInt(homeScore) && homeId == currTeamId);
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