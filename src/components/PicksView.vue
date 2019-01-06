<template>
    <div class="card boxShadow blueOutline" v-if="loggedIn() && hasMadePicks()">
        <h2>{{getUserName()}}'s Picks</h2>
        <div 
            style="display: flex; 
                align-items: center; 
                flex-direction: row;
                height: 50px"
            v-for="player in this.getPicks" :key="player.playerId"
            :class="[player.isSeason ? 'card-row unplayedGameRow' : 'card-row activeGameRow' ]"
            @click="goToPlayer(player.playerId)"
            >
            <img :class="[player.isSeason ? 'card-row-logo grayImg' : 'card-row-logo']" 
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
                <span class="b">{{ player.isSeason ? Math.round(player.fpts/player.gameCount) : player.fpts }} </span>
                <span class="statLabel">{{ player.isSeason ? "FPPG" : "FPTS"}}</span>
            </div>
            <div class="players-pts">
                <span class="b">{{  player.isSeason ? Math.round(player.pts/player.gameCount) : player.pts }} </span>
                <span class="statLabel">{{ player.isSeason ? "PPG" : "PTS"}}</span>
            </div>
            <div class="players-reb">
                <span class="b">{{  player.isSeason ? Math.round(((parseInt(player.offReb)+parseInt(player.defReb))/player.gameCount)) : (parseInt(player.offReb)+parseInt(player.defReb)) }} </span>
                <span class="statLabel">{{ player.isSeason ? "RPG" : "REB"}}</span>
            </div>
            <div class="players-ast">
                <span class="b">{{  player.isSeason ? Math.round(player.ast/player.gameCount) : player.ast }} </span>
                <span class="statLabel">{{ player.isSeason ? "APG" : "AST"}}</span>
            </div>
            <div class="players-stl">
                <span class="b">{{  player.isSeason ? Math.round(player.stl/player.gameCount) : player.stl }} </span>
                <span class="statLabel">{{ player.isSeason ? "SPG" : "STL"}}</span>
            </div>
            <div class="players-blk">
                <span class="b">{{  player.isSeason ? Math.round(player.blk/player.gameCount) : player.blk }} </span>
                <span class="statLabel">{{ player.isSeason ? "BPG" : "BLK"}}</span>
            </div>
            <div class="players-tov">
                <span class="b">{{  player.isSeason ? Math.round(player.tov/player.gameCount) : player.tov }}</span>
                <span class="statLabel">{{ player.isSeason ? "TPG" : "TOV"}}</span>
            </div>
            <div class="players-foulPers">
                <span class="b">{{  player.isSeason ? Math.round(player.foulPers/player.gameCount) : player.foulPers }} </span>
                <span class="statLabel">{{ player.isSeason ? "FPG" : "FLS"}}</span>
            </div>
            <div class="players-plusMinus">
                <span class="b">{{  player.plusMinus }}</span>
                <span class="statLabel">{{ player.isSeason ? "TPM" : "PM"}}</span>
            </div>
            <div class="players-mins">
                <span class="b">{{  player.isSeason ? convertToMinSec(player.minSeconds/player.gameCount) : convertToMinSec(player.minSeconds) }} </span>
                <span class="statLabel">{{ player.isSeason ? "MPG" : "MIN"}}</span>
            </div>
        </div>
        <button v-if="canChangePicks()" @click="goToPickPage()" style="margin: 20px" class="loginButton">Change</button>       
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PicksView",
    computed: {
        getPicks() {
            return store.state.picks;
        }
    },
    data: function() {
        return {
            picks: {
                PG: -1, 
                SG: -1, 
                SF: -1, 
                PF: -1, 
                C: -1
            },
        }
    },
    methods: {
        hasMadePicks: function() {
            return store.state.picks.length == 5;
        },
        getUserName: function() {
            return sessionStorage.getItem('username');
        },
        loggedIn: function() {
            return sessionStorage.getItem('token') != null
        },
        canChangePicks: function() {
            return store.state.picks.filter(p => p.isSeason).length == 5;
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        goToPickPage: function() {
            router.push('/pick/');
        },
        convertToMinSec: function(minSeconds) {
            return Math.floor(minSeconds/60);
        },
        setPlayerData: function() {
            console.log(store.state.apiDataPlayers);
            this.playerData.PG = store.state.apiDataPlayers.filter(s => s.playerId == playerData.PG);
        },
        getMadePicks: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getUserPicks.php?current&username='+sessionStorage.getItem('username');
            // console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    if (responseData.length != 5) return;
                    store.commit('setPicks', responseData);
            });
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
    },
    beforeRouteUpdate(to, from, next) {
        this.getMadePicks();
        next();
    },
    watch: {
        $route (to, from) {
            this.getMadePicks();
        }
    },
    created() {
        this.getMadePicks();
    }
};
</script>