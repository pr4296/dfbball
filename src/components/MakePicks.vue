<template>
<div class="card boxShadow">
    <p class="card-header">Make Picks</p>
    <div class="playerPickDiv">
        <select 
            class="playerSelect" 
            v-model="picks.PG"> 
            <option disabled value="-1">Point Guard</option> 
            <option 
                v-for="player in this.players('PG')" 
                v-bind:value="player.playerId" 
                :key="player.playerId">

                {{player.firstName+' '+player.lastName}}
            </option>
        </select>
        <select class="playerSelect" v-model="picks.SG">
            <option disabled value="-1">Shooting Guard</option> 
            <option v-for="player in this.players('SG')" v-bind:value="player.playerId" :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" v-model="picks.SF">
            <option disabled value="-1">Small Forward</option> 
            <option v-for="player in this.players('SF')" v-bind:value="player.playerId"  :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" v-model="picks.PF">
            <option disabled value="-1">Power Forward</option> 
            <option v-for="player in this.players('PF')" v-bind:value="player.playerId"  :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <select class="playerSelect" v-model="picks.C">
            <option disabled value="-1">Center</option> 
            <option v-for="player in this.players('C')" v-bind:value="player.playerId"  :key="player.playerId">{{player.firstName+' '+player.lastName}}</option>
        </select>
        <span class="errorMessage">{{errorMessage}}</span>
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
            picks: {
                PG: -1, 
                SG: -1, 
                SF: -1, 
                PF: -1, 
                C: -1
            },
            errorMessage: ""
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
        makePlayerPicks: function() {
            var url = 'https://pratyush.rustagi.cc/dfbball/api/makePicks.php?token='+sessionStorage.getItem('token')+'&username='+sessionStorage.getItem('username')+'&PG='+this.picks.PG+'&SG='+this.picks.SG+'&SF='+this.picks.SF+'&PF='+this.picks.PF+'&C='+this.picks.C;
            console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    if (responseData.message != 'success') {
                        vm.errorMessage = responseData.message;
                    }
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        makePicks: function() {
            console.log(this.picks);
            if (this.picks.PG == -1 || this.picks.SG == -1 || this.picks.SF == -1 || this.picks.PF == -1 || this.picks.C == -1) {
                this.errorMessage = "Pick a player at each position.";
                return false;
            }
            else if (this.picks.PG == this.picks.SG || this.picks.SF == this.picks.PF) {
                this.errorMessage = "Each player picked must be unique.";
                return false;
            }
            this.errorMessage = "";
            this.makePlayerPicks();

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