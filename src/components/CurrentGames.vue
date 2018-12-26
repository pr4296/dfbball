<template>
    <div  class="card boxShadow">
        <p class="card-header">Schedule</p>
        <div class="gameRow" 
            v-for="(game, index) in this.games" :key="index"
            @click="goToGame(game.id)"
            >
            <div class="scoreColumn">
                <div class="teamRow">
                    <div class="logoWrapper">
                        <img 
                            class="card-row-logo" 
                            :src="logoUrl(game.awayTeamAbbreviation)"> 
                    </div>
                    <div class="teamRecord">
                        {{ getWinLoss(game.awayTeamId) }}
                    </div>
                    <div class="teamRanking" :class="isEastern(game.awayTeamId) ? 'easternRankingBadge rankingBadge' : 'westernRankingBadge rankingBadge'">
                        {{ getRanking(game.awayTeamId )}}
                    </div>
                    <div class="card-row-text b teamNameWrapper" >
                        <span class="teamCity">
                            {{ game.awayCity }}
                        </span>
                        {{ game.awayTeamName }}
                    </div>
                    <div class="teamScoreWrapper">
                        <span class="card-row-text b" >
                        {{ game.awayScoreTotal }}
                        </span>
                    </div>
                </div>
                <div class="teamRow">
                    <div class="logoWrapper">
                        <img 
                            class="card-row-logo" 
                            :src="logoUrl(game.homeTeamAbbreviation)"> 
                    </div>
                    <div class="teamRecord">
                        {{ getWinLoss(game.homeTeamId) }}
                    </div>
                    <div class="teamRanking" :class="isEastern(game.homeTeamId) ? 'easternRankingBadge rankingBadge' : 'westernRankingBadge rankingBadge'">
                        {{ getRanking(game.homeTeamId )}}
                    </div>
                    <div class="card-row-text b teamNameWrapper" >
                        <span class="teamCity">
                        {{ game.homeCity }}
                        </span>
                        {{ game.homeTeamName }}
                    </div>
                    <div class="teamScoreWrapper">
                        <span class="card-row-text b">
                        {{ game.homeScoreTotal }}
                        </span>
                    </div>
                </div>
            </div>
            <div class="gameStatus gray" v-bind:class="{ liveGameGreen: isGameLive(game) }"> 
                    {{ getGameStatus(game) }}
            </div>
            <div class="game-top-player-container">
                <GameTopPlayer :gameIndex="index" :game="games"></GameTopPlayer>
            </div>
        </div>
    </div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import GameTopPlayer from "@/components/GameTopPlayer.vue"

export default {
    name: "Players",
    components: {
        GameTopPlayer
    },
    computed: {
        games: function() {
            return store.state.apiDataCurrentGames
        },
    },
    methods: {
        getWinLoss: function(teamId) {
            var foundTeam = store.state.apiDataTeams.find(x => x.id === teamId);
            if (!foundTeam) return "";
            var wins = foundTeam.wins;
            var losses = foundTeam.losses;
            return "("+wins+"-"+losses+")";
        },
        getRanking: function(teamId) {
            //console.log(teamId, "in getRanking");
            var foundTeam = store.state.apiDataTeams.find(x => x.id === teamId);
            //console.log(store.state.apiDataTeams);
            //console.log('found team', foundTeam);
            if (!foundTeam) return "";
            //console.log(foundTeam.conferenceRank);
            return foundTeam.conferenceRank;
        },
        isEastern: function(teamId) {
            var foundTeam = store.state.apiDataTeams.find(x => x.id === teamId);
            if (!foundTeam) return "";
            return foundTeam.conferenceName === 'Eastern';
        },
        isGameLive: function(game) {
            var s = this.getGameStatus(game);
            return s[0] === 'Q' || s[0] == 'O';
        },
        getGameStatus: function(gameRow) {
            if (gameRow['playedStatus'] == "LIVE")
            {
                var intermission = gameRow['currentIntermission'];
                if (intermission == "NULL") {
                    if (gameRow['currentQuarter'] == null && gameRow['currentQuarterSecondsRemaining'] == null) return "Starting";
                    // use format of Q1 3:43
                    var secRem = parseInt(gameRow['currentQuarterSecondsRemaining']);
                    var res = "Q"+gameRow['currentQuarter']+" - "
                    if (gameRow['currentQuarter'] > 5) {
                        res = (parseInt(gameRow['currentQuarter'])-4)+"OT - ";
                    }
                    else if (gameRow['currentQuarter'] == 5) {
                        res = "OT - ";
                    }
                    res += Math.floor(secRem/60)+":"+(secRem%60 < 10 ? "0"+(secRem%60) : (secRem%60));

                    return res;
                }
                else {
                    if (intermission == "2") return "Halftime";
                    else if (intermission == "1") return "End Q1";
                    else if (intermission == "3") return "End Q3";
                    else if (intermission == "4" && gameRow['awayScoreTotal'] != gameRow['homeScoreTotal']) return "End Q4";
                    else if (intermission == "4" && gameRow['awayScoreTotal'] == gameRow['homeScoreTotal']) return "Final";
                }
            }
            else if (gameRow['playedStatus'] == "UNPLAYED") {
                gameRow['currentQuarter']

                var utcDatePlusOffset = new Date(gameRow['startTime']);
                var offset = utcDatePlusOffset.getTimezoneOffset();
                var gameDateFull = new Date(utcDatePlusOffset-offset*60*1000);

                var gameTime = gameDateFull.toLocaleTimeString();
                gameTime = gameTime.substring(0, gameTime.length-6)+" "+gameTime.substring(gameTime.length-2, gameTime.length);  
                
                return gameTime;
            }
            return "Final";
            
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        fetchCurrentGames: function() {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/currentGames.php?dayDiff=2';
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    // console.log(responseData);
                    store.commit('setApiDataCurrentGames', responseData);
            });
        },
        fetchGameTopPlayers: function(gameId) {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getGameTopPlayers.php';
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    store.commit('setApiDataGameTopPlayers', responseData);
            });
        },
        goToGame: function(gameId) {
            router.push('/game/'+gameId)
        },
        goToTeam: function(teamId) {
            router.push('/team/'+teamId)
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchCurrentGames();
        this.fetchGameTopPlayers();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchCurrentGames();
            this.fetchGameTopPlayers();
        }
    },
    created() {
        this.fetchCurrentGames();
        this.fetchGameTopPlayers();
    }
}
</script>