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
                <th class="boxscore-stl">STL</th>
                <th class="boxscore-blk">BLK</th>
                <th class="boxscore-fg">FG</th>
                <th class="boxscore-3pt">3PT</th>
                <th class="boxscore-ft">FT</th>
                <th class="boxscore-tov">TOV</th>
                <th class="boxscore-fls">FLS</th>
                <th class="boxscore-pm">+/-</th>
                <th class="boxscore-min">MIN</th>
            </thead>
            <tbody>
                <tr v-for="row in this.boxStats" :key="row.gameId"
                    @click="goToGame(row.gameId)">
                    <td><span :class="[wonGame(row.awayScoreTotal, row.homeScoreTotal, row.awayTeamId, row.homeTeamId, row.playerTeamId) ? 'boxscore-win' : 'boxscore-loss' ]">
                        {{ wonGame(row.awayScoreTotal, row.homeScoreTotal, row.awayTeamId, row.homeTeamId, row.playerTeamId) ? 'W' : 'L' }}
                        </span>
                    </td>
                    <td>{{ row.atOrVs }}{{ row.opposingTeamAbbreviation }}</td>
                    <td style="font-size: 12px;">{{ getLocalGameTime(row.startTime) }}</td>
                    <td :style="getBgColor(row.pts, 10)">{{ row.pts }}</td>
                    <td :style="getBgColor(parseInt(row.offReb)+parseInt(row.defReb), 3)">{{ parseInt(row.offReb)+parseInt(row.defReb) }}</td>
                    <td :style="getBgColor(row.ast, 3)">{{ row.ast }}</td>
                    <td class="boxscore-stl" :style="getBgColor(row.stl, 0.6)">{{ row.stl }}</td>
                    <td class="boxscore-blk" :style="getBgColor(row.blk, 0.6)">{{ row.blk }}</td>
                    <td class="boxscore-fg" :style="getBgColor(
                        ( parseInt(row.fg2PtMade)+ parseInt(row.fg3PtMade))*
                        (parseInt(row.fg2PtMade)+parseInt(row.fg3PtMade))/(parseInt(row.fg2PtAtt)+parseInt(row.fg3PtAtt)), 3)">{{ parseInt(row.fg2PtMade)+parseInt(row.fg3PtMade) }}/{{ parseInt(row.fg2PtAtt)+parseInt(row.fg3PtAtt) }}</td>
                    <td class="boxscore-3pt" :style="getBgColor(row.fg3PtMade*row.fg3PtMade/row.fg3PtAtt, 1)">{{ row.fg3PtMade }}/{{ row.fg3PtAtt }}</td>
                    <td class="boxscore-ft" :style="getBgColor(row.ftMade*row.ftMade/row.ftAtt, 2)">{{ row.ftMade }}/{{ row.ftAtt }}</td>
                    <td class="boxscore-tov" :style="getBgColor(0.4, row.tov*0.2)">{{ row.tov }}</td>
                    <td class="boxscore-fls" :style="getBgColor(0.4, row.foulPers*0.2)">{{ row.foulPers }}</td>
                    <td class="boxscore-pm" :style="getBgColor(parseInt(row.plusMinus)+5, 5)">{{ row.plusMinus }}</td>
                    <td class="boxscore-min" :style="getBgColor(row.minSeconds, 60*10)">{{ Math.ceil(row.minSeconds/60) }}</td>
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
        getBgColor: function(val, avg) {
            avg = avg*1.01;
            val = val*0.99;
            var r = Math.max(Math.min(126*(val/avg-0.25)+160, 255), 0);
            var g = val/avg > 1 ? Math.max(Math.min((4-val/avg)*75+30, 255), 0) : Math.max(Math.min((4-val/avg)*18+200, 255), 0);
            var b = Math.max(Math.min((4-val/avg)*75+30, 255), 0);
            
            //4x = rgb(255, 30, 30)
            //1x = rgb(255, 255, 255)
            //0.25 = rgb(160, 200, 255)

            var toRet = "background-color: rgb("+r+", "+g+", "+b+", 0.8)";
            if (r > 240 && g < 60) {
                console.log('toret',r,g);
                toRet = "color: #fff; font-weight: 600; "+toRet;
            }
            return toRet;
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