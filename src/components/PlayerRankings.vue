<template>
<div class="card boxShadow">
    <p class="card-header">Player Rankings</p>
    <div 
        v-for="player in players" :key="player.playerId"
        @click="goToPlayer(player.playerId)">
        <span 
            class="card-row-text"> 
                <span class="b">
                    {{ player.firstName }} 
                    {{ player.lastName }}
                </span>
                <span>
                    {{ player.rank_pts }}
                </span>
        </span>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PlayerRankings",
    props: {
        teamId: {}
    },
    computed: {
        players: function() {
            return this.getTopPlayers('rank_pts', 3);
        }
    },
    methods: {
        fetchPlayerRankings: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerRankings.php'
            if (this.$props.teamId.length > 0) url += "?teamId="+this.$props.teamId;
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    store.commit('setPlayerRankings', responseData);
            });
        },
        goToPlayer: function(playerId) {
            router.push('/player/'+playerId)
        },
        getTopPlayers(columnName, resultSize) {
            console.log("inside getTopPlayers");
            var res = store.state.playerRankings;
            var res = res.sort((a, b) => parseInt(a[columnName]) - parseInt(b[columnName]) );
            return res.slice(0, resultSize);
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchPlayerRankings();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchPlayerRankings();
        }
    },
    created() {
        this.fetchPlayerRankings();
    }
}
</script>