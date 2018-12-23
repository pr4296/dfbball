<template>
  <div class="card boxShadow">
        <p class="card-header">Top Players</p>
        <div 
            class="card-row" 
            v-for="player in this.players" :key="player.id"
            @click="goToPlayer(player.id)">
            <img class="card-row-logo" 
                :src="logoUrl(player.abbreviation)">
            <div> {{ player.primaryPosition }} </div>
            <div class="b"> 
                <span>{{ player.firstName }}</span>
                <span>{{ player.firstName.substring(0, 1)+"." }}</span>
                <span>{{ player.lastName }}</span>
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