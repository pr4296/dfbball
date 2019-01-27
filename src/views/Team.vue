<template>
<div>
    <div class="container">
        <div style="display: flex;"><img style="height: 30px;  margin: auto; margin-right: 20px;" :src="logoUrl(this.teamInfo.abbreviation)">
            <span style="font-size: 25px; font-weight: bolder">{{ this.teamInfo.city }} {{ this.teamInfo.teamName }}</span>
        </div>
        <PlayerRankings :teamId="this.$route.params.id" ></PlayerRankings>
        <TeamUpcomingGames></TeamUpcomingGames>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import TeamUpcomingGames from "@/components/TeamUpcomingGames.vue";
import PlayerRankings from "@/components/PlayerRankings.vue";

export default {
    name: "Team",
    components: {
        TeamUpcomingGames,
        PlayerRankings
    },
    computed: {
        teamInfo: function() {
            return store.state.apiDataTeam
        },
        upcomingGames: function() {
            console.log(store.state.apiDataUpcomingGames)
            return store.state.apiDataUpcomingGames
        }
    },
    methods: {
        fetchTeam: function() {
            console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/teams.php?id='+this.$route.params.id;
            console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    // console.log(responseData);
                    store.commit('setApiDataTeam', responseData[0]);
            });
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        }
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchTeam();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchTeam();
        }
    },
    created() {
        this.fetchTeam();
    }
};
</script>