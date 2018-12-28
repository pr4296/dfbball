<template>
    <div class="card boxShadow">
        <h2>Daily Picks</h2>
       <span v-text="this.playerData.PG.pts"></span>
       <span v-text="this.playerData.SG.pts"></span>
       <span v-text="this.playerData.SF.pts"></span>
       <span v-text="this.playerData.PF.pts"></span>
       <span v-text="this.playerData.C.pts"></span>
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PicksView",
    data: function() {
        return {
            picks: {
                PG: -1, 
                SG: -1, 
                SF: -1, 
                PF: -1, 
                C: -1
            },
            playerData: {
                PG: {}, 
                SG: {}, 
                SF: {}, 
                PF: {}, 
                C: {}
            },
        }
    },
    methods: {
        setPlayerData: function() {
            console.log(store.state.apiDataPlayers);
            this.playerData.PG = store.state.apiDataPlayers.filter(s => s.playerId == playerData.PG);
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
                    vm.picks.PG = responseData[0];
                    vm.picks.SG = responseData[1];
                    vm.picks.SF = responseData[2];
                    vm.picks.PF = responseData[3];
                    vm.picks.C = responseData[4];
                    console.log(responseData, vm.picks.PG);
            });
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