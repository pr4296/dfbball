<template>
    <div v-if="this.players.length > 0" class="card boxShadow">
        <p class="card-header">Top Players</p>
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
                <span class="b">{{ player.overallRating }} </span>
                <span class="statLabel">OVR</span>
            </div>
            <div class="players-pts">
                <span class="b">{{ player.offRating }} </span>
                <span class="statLabel">OFF</span>
            </div>
            <div class="players-reb">
                <span class="b">{{ player.defRating }} </span>
                <span class="statLabel">DEF</span>
            </div>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "Players",
    computed: {
        players: function() {
            return store.state.apiDataTopPlayers
        }
    },
    methods: {
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        fetchTopPlayers: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getPlayerCards.php';
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setApiDataTopPlayers', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        convertToMinSec: function(minSeconds) {
            return Math.floor(minSeconds/60)+1;
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
};
</script>