<template>
<div class="card boxShadow" v-if="visible()">
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
        <button id="btnMakePicks" class="loginButton" type="button" v-on:click="makePicks()" v-text="this.buttonText"></button>
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
            errorMessage: "",
            buttonText: "Pick Players"
        }
    },
    methods: {
        visible() {
            return sessionStorage.getItem('username') != null;
        },
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
                    // console.log(responseData);
                    store.commit('setAvailablePlayerPicks', responseData);
                    console.log(responseData);
            });
        },
        getMadePicks: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getUserPicks.php?username='+sessionStorage.getItem('username');
            // console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    if (responseData.length != 5) return;
                    vm.picks.PG = responseData[0].playerId;
                    vm.picks.SG = responseData[1].playerId;
                    vm.picks.SF = responseData[2].playerId;
                    vm.picks.PF = responseData[3].playerId;
                    vm.picks.C = responseData[4].playerId;
                    vm.buttonText = "Update Picks";
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
                    else {
                        vm.buttonText = "Success";
                        var btn = document.getElementById('btnMakePicks');
                        btn.style.backgroundColor = "#0e8";
                        btn.disabled = true;
                        setTimeout(function(){ 
                            vm.buttonText = "Update Picks";
                            btn.style.backgroundColor = "#278cff";
                            btn.disabled = false;
                         }, 2000);
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
        },
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
        this.getMadePicks();
    }
}
</script>