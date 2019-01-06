<template>
    <div v-if="this.players.length > 0" class="card boxShadow">
        <p class="card-header">Recent Top Players</p>
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
            <div class="players-reb">
                <span class="b">{{ (parseInt(player.offReb)+parseInt(player.defReb)) }} </span>
                <span class="statLabel">REB</span>
            </div>
            <div class="players-ast">
                <span class="b">{{ player.ast }} </span>
                <span class="statLabel">AST</span>
            </div>
            <div class="players-stl">
                <span class="b">{{ player.stl }} </span>
                <span class="statLabel">STL</span>
            </div>
            <div class="players-blk">
                <span class="b">{{ player.blk }} </span>
                <span class="statLabel">BLK</span>
            </div>
            <div class="players-tov">
                <span class="b">{{ player.tov }} </span>
                <span class="statLabel">TOV</span>
            </div>
            <div class="players-foulPers">
                <span class="b">{{ player.foulPers }} </span>
                <span class="statLabel">FLS</span>
            </div>
            <div class="players-plusMinus">
                <span class="b">{{ player.plusMinus }} </span>
                <span class="statLabel">PM</span>
            </div>
            <div class="players-mins">
                <span class="b">{{ convertToMinSec(player.minSeconds) }} </span>
                <span class="statLabel">MIN</span>
            </div>

        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "DailyTopPlayers",
    computed: {
        players: function() {
            return store.state.apiDataDailyTopPlayers
        }
    },
    methods: {
        convertToMinSec: function(minSeconds) {
            return Math.floor(minSeconds/60);
        },
        fetchTopPlayers: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/todaysTopPlayers.php';
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setApiDataDailyTopPlayers', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchTopPlayers();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchTopPlayers();
        }
    },
    created() {
        this.fetchTopPlayers();
    }
}
</script>