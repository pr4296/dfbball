<template>
<div>
    <p>Team {{ this.teamInfo.city }} {{ this.teamInfo.teamName }}</p>
    <p>Arena: {{ this.teamInfo.venueName }}</p>
    <div class="card-container">
        <TeamUpcomingGames></TeamUpcomingGames>
        <TeamRoster></TeamRoster>
    </div>
</div>
</template>

<script>

import store from "@/store.js";
import router from "@/router.js";
import TeamUpcomingGames from "@/components/TeamUpcomingGames.vue";
import TeamRoster from "@/components/TeamRoster.vue";

export default {
    name: "Team",
    components: {
        TeamUpcomingGames,
        TeamRoster
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