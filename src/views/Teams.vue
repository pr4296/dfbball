<template>
<div class="container">
    <div class="standingsContainer">
        <div class="card boxShadow">
            <p class="card-header">Eastern Conference</p>
            <div 
                class="gameRow" 
                v-for="team in easternTeams()" :key="team.id"
                @click="goToTeam(team.id)">

                <span class="card-row-text">{{ team.conferenceRank }}</span>
                <img 
                    class="card-row-logo" 
                    :src="logoUrl(team.abbreviation)"
                    >
                <div class="team-name card-row-text">
                    <span class="b team-city">{{ team.city }} </span>
                    <span class="b">{{ team.teamName }}</span>
                </div>
                <div class="team-gamesback">
                    <span class="b">{{ team.conferenceGamesBack }}</span>
                    <span class="statLabel">GB</span>
                </div>
                <div class="team-wins">
                    <span class="b">{{ team.wins }}</span>
                    <span class="statLabel">W</span>
                </div>
                <div class="team-losses">
                    <span class="b">{{ team.losses }}</span>
                    <span class="statLabel">L</span>
                </div>
                <div class="team-winpct">
                    <span class="b">{{ team.winPct }}</span>
                    <span class="statLabel">WIN%</span>
                </div>
                <div class="team-overallrank">
                    <span class="b">{{ team.overallRank }}</span>
                    <span class="statLabel">OVR</span>
                </div>
            </div>
        </div>
        <div class="card boxShadow">
            <p class="card-header">Western Conference</p>
            <div 
                class="gameRow" 
                v-for="team in westernTeams()" :key="team.id"
                @click="goToTeam(team.id)">

                <span class="card-row-text">{{ team.conferenceRank }}</span>
                <img 
                    class="card-row-logo" 
                    :src="logoUrl(team.abbreviation)"
                    >
                <div class="team-name card-row-text">
                    <span class="b team-city">{{ team.city }} </span>
                    <span class="b">{{ team.teamName }}</span>
                </div>
                <div class="team-gamesback">
                    <span class="b">{{ team.conferenceGamesBack }}</span>
                    <span class="statLabel">GB</span>
                </div>
                <div class="team-wins">
                    <span class="b">{{ team.wins }}</span>
                    <span class="statLabel">W</span>
                </div>
                <div class="team-losses">
                    <span class="b">{{ team.losses }}</span>
                    <span class="statLabel">L</span>
                </div>
                <div class="team-winpct">
                    <span class="b">{{ team.winPct }}</span>
                    <span class="statLabel">WIN%</span>
                </div>
                <div class="team-overallrank">
                    <span class="b">{{ team.overallRank }}</span>
                    <span class="statLabel">OVR</span>
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
    name: "Teams",
    computed: {
        allTeams: function() {
            return store.state.apiDataTeams;
        }
    },
    methods: {
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
        goToTeam: function(teamId) {
            router.push('/team/'+teamId)
        },
        easternTeams: function() {
            var subset = this.allTeams.filter(t => t.conferenceName === "Eastern");
            subset.sort(function(a, b) { 
                return parseInt(a.conferenceRank) - parseInt(b.conferenceRank); 
            });
            return subset;
        },
        westernTeams: function() {
            var subset = this.allTeams.filter(t => t.conferenceName === "Western");
            subset.sort(function(a, b) { 
                return parseInt(a.conferenceRank) - parseInt(b.conferenceRank); 
            });
            return subset;
        }
    }
}
</script>