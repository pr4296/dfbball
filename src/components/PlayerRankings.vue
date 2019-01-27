<template>
<div>
    <div class="card boxShadow">
        <p class="card-header">Top Fantasy Players</p>
        <div 
            v-for="player in top_fpts" :key="player.playerId"
            @click="goToPlayer(player.playerId)" style="cursor: pointer">
            <div class="topPlayerTinyCard">
                <img style="align-self: flex-end; height: 80px" :src="player.imgUrl"/>
                <div style="display: flex; flex-direction: column; padding: 10px;">
                    <span class="b">
                        {{ player.firstName }} 
                        {{ player.lastName }}
                    </span>
                    <span>
                        {{ Math.round(parseFloat(player.fpts)*100/parseFloat(player.gameCount))/100.0 }} FPPG
                    </span>
                    <span>
                        #<span style="font-weight: bolder">{{ player.rank_fpts }}</span> Overall Rank
                    </span>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PlayerRankings",
    props: {
        teamId: {},
        numResults: {},
    },
    computed: {
        top_fpts: function() {
            return this.getTopPlayers('rank_fpts', 3);
        }
    },
    methods: {
        fetchPlayerRankings: function() {
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerRankings.php'
            if (this.$props.teamId != undefined) url += "?teamId="+this.$props.teamId;
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
        getTopPlayers(columnName) {
            console.log("inside getTopPlayers");
            var res = store.state.playerRankings;
            var res = res.sort((a, b) => parseInt(a[columnName]) - parseInt(b[columnName]) );
            return res.slice(0, this.$props.numResults == undefined ? 3 : this.$props.numResults);
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