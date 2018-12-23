<template>
<div class="card boxShadow">
    <p class="card-header">Roster</p>
    <div 
        class="card-row" 
        v-for="player in this.players" :key="player.id"
        @click="goToPlayer(player.id)"
        :class="[
            player.overallRating >= 95 ? 'borderPinkDiamond' : '',
            player.overallRating < 95 && player.overallRating >= 92 ? 'borderSapphire' : '',
            player.overallRating < 92 && player.overallRating >= 88 ? 'borderRuby' : '',
            player.overallRating < 88 && player.overallRating >= 85 ? 'borderEmerald' : '',
            player.overallRating < 85 && player.overallRating >= 75 ? 'borderGold' : '',
            player.overallRating < 75 && player.overallRating >= 65 ? 'borderSilver' : '',
            player.overallRating < 65 ? 'borderBronze' : ''
        ]"
        >
        <span 
            class="card-row-text"> 
                {{ player.primaryPosition }}
                #{{ player.jerseyNumber }}
                <span class="b">
                    {{ player.firstName }} 
                    {{ player.lastName }}
                </span>
                <span>
                    {{ player.overallRating }}
                    ({{ player.offRating }}/{{ player.defRating }})
                </span>
        </span>
    </div>
</div>
</template>

<script>

import TeamUpcomingGames from "@/components/TeamUpcomingGames.vue";
import TeamRoster from "@/components/TeamRoster.vue";
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "Team",
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
            var url = 'https://pratyush.rustagi.cc/basketbrief/api/getPlayerCards.php?teamId='+this.$route.params.id;
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