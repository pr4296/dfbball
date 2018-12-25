<template>
<div class="card boxShadow">
    <p class="card-header">Make Picks</p>
    <div>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "MakePicks",
    computed: {
        players: function() {
            console.log('inside computed players');
            console.log(store.state.apiDataRouter);
            return store.state.apiDataRoster
        }
    },
    methods: {
        fetchRoster: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/getPlayerCards.php?teamId='+this.$route.params.id;
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setApiDataRoster', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchRoster();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchRoster();
        }
    },
    created() {
        this.fetchRoster();
    }
}
</script>