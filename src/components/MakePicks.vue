<template>
<div class="card boxShadow">
    <p class="card-header">Make Picks</p>
    <div class="playerPickDiv">
        <select class="playerSelect" >
            <option v-for="player in this.players('PG')" v-bind:value="picks[0]" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" > 
            <option v-for="player in this.players('SG')" v-bind:value="picks[1]" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" >
            <option v-for="player in this.players('SF')" v-bind:value="picks[2]" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" >
            <option v-for="player in this.players('PF')" v-bind:value="picks[3]" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" >
            <option v-for="player in this.players('C')" v-bind:value="picks[4]" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <button class="loginButton" type="button" v-on:click="makePicks()">Pick Players</button>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "MakePicks",
    data: function() {
        return {
            picks: [0, 0, 0, 0, 0]
        }
    },
    methods: {
        players: function(pos) {
            if (pos == 'PG')
                return store.state.availablePlayerPicks.filter(p => p.primaryPosition == 'PG' || p.primaryPosition == 'G');
            else if (pos == 'SG')
                return store.state.availablePlayerPicks.filter(p => p.primaryPosition == 'SG' || p.primaryPosition == 'G');
            else if (pos == 'SF')
                return store.state.availablePlayerPicks.filter(p => p.primaryPosition == 'SF' || p.primaryPosition == 'F');
            else if (pos == 'PF')
                return store.state.availablePlayerPicks.filter(p => p.primaryPosition == 'PF' || p.primaryPosition == 'F');
            else if (pos == 'C')
                return store.state.availablePlayerPicks.filter(p => p.primaryPosition == 'C');
            return store.state.availablePlayerPicks;
        },
        fetchAvailablePlayers: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getAvailablePlayerPicks.php';
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setAvailablePlayerPicks', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        makePicks: function() {
            console.log(this.picks);
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchAvailablePlayers();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchAvailablePlayers();
        }
    },
    created() {
        this.fetchAvailablePlayers();
    }
}
</script>