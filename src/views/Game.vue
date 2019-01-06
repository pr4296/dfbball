<template>
<div style="display: inline-flex; flex-direction: column">
  <div class="card boxShadow">
    <div class="gameRow">
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
  </div>
  </div>
  <div v-if="this.players.length > 0" class="card boxShadow">
      <p class="card-header">Players</p>
      <div 
          class="card-row" 
          style="display: flex; 
              align-items: center; 
              flex-direction: row;
              height: 50px"
          v-for="player in this.players" :key="player.playerId"
          @click="goToPlayer(player.playerId)"
          >
          <img class="card-row-logo" 
              :src="logoUrl(player.abbreviation)">
          <div class="playerName">
              <span 
                  class="card-row-text"
                  style="flex: 1 0 auto"> 
                      <span style="font-size: 1.3em" class="b players-firstName">
                          {{ player.firstName }} 
                      </span>
                      <span style="font-size: 1.3em" class="b players-firstNameInitial">
                          {{ player.firstName.substring(0, 1)+"." }} 
                      </span>
                      <span style="font-size: 1.3em" class="b">
                          {{ player.lastName }}
                      </span>
              </span>
          </div>
          <div class="players-fpts">
              <span class="b">{{ player.fpts }} </span>
              <span class="statLabel">FPTS</span>
          </div>
          <div class="players-pts">
              <span class="b">{{ player.pts }} </span>
              <span class="statLabel">PTS</span>
          </div>
          <div class="players-mins">
              <span class="b">{{ convertToMinSec(player.minSeconds) }} </span>
              <span class="statLabel">MIN</span>
          </div>
      </div>
  </div>
</div>
</template>


<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "game",
    computed: {
        players: function() {
            return store.state.apiDataGamePlayers.players
        },
        game: function() {
            return store.state.apiDataGamePlayers.gameInfo
        }
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
        fetchGameInfo: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getGameInfo.php?id='+this.$route.params.id;
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setApiDataGamePlayers', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        convertToMinSec: function(minSeconds) {
            return Math.floor(minSeconds/60);
        },
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchGameInfo();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchGameInfo();
        }
    },
    created() {
        this.fetchGameInfo();
    }
};
</script>