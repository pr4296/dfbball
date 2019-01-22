<template>
    <div class="playerCard">
        <div style="background: #444; display: flex">
             <img 
                  style="width: 50px; position: absolute; margin: 10px;"
                  :src="logoUrl(this.player.abbreviation)"> 
            <img class="playerCardImage" style="align-self: flex-end" :src="this.player.imgUrl"/>
        </div>
        <div class="statBox" style="color: white;">
            <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-end; margin-bottom: 20px">
                <span style="display: inherit; font-size: 20px; font-weight: bold">{{ this.player.firstName }} {{this.player.lastName }}</span>
                <div><span style="font-weight: bolder">#{{ this.player.jerseyNumber }}</span></div>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: flex-start; align-items: flex-end; margin-bottom: 10px">
                <div style="margin-right: 10px">
                    <span style="color: #999">Position </span>
                    <span style="font-weight: bolder">{{ getFullPositionName(this.player.primaryPosition) }}</span>
                </div>
                <div>
                    <span style="color: #999; ">Age </span>
                    <span style="font-weight: bolder">{{getAgeInYears(this.player.birthDate)}}</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: flex-start; align-items: flex-end; margin-bottom: 10px">
                <div style="margin-right: 10px">
                    <span style="color: #999">Height </span> 
                    <span style="font-weight: bolder"> {{ getHeightString(this.player.heightInches)}} </span>
                </div>
                <div>
                    <span style="color: #999">Weight </span>
                    <span style="font-weight: bolder"> {{this.player.weightPounds}} lbs</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: flex-start; align-items: flex-end; margin-bottom: 10px">
                <span style="color: #999; margin-right: 3px">Contract </span>
                <span style="font-weight: bolder"> {{ getSalaryString(this.player.contractYearsCount, this.player.contractTotalSalary)}}</span>
            </div>
            <div style="display: flex; flex-direction: row; justify-content: flex-start; align-items: flex-end; margin-bottom: 10px">
                <span style="color: #999; margin-right: 3px">School </span>
                <span style="font-weight: bolder"> {{ getRecentSchool(this.player.highSchool, this.player.college)}}</span>
            </div>
            
            <span></span>
            
        </div>
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PlayerCard",
    props: ['playerId'],
    computed: {
        player: function() {
            return store.state.playerCard[0];
        }
    },
    methods: {
        fetchPlayer: function() {
            console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerInfo.php?id='+this.$route.params.id;
            // console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log('player stuff',responseData);
                    store.commit('setPlayerCard', responseData);
            });
        },
        getFullPositionName: function(posAbbrv) {
            var dict = {'PG': 'Point Guard', 'G': 'Guard', 'SG': 'Shooting Guard', 'SF': 'Small Forward', 'F': 'Forward', 'PF': 'Power Forward', 'C': 'Center'};
            return dict[posAbbrv];
        },
        roundSalary: function(total) {
            console.log('total',total);
            if (total < 1000000) return Math.round(total/1000)+'K';
            else if (total < 10000000) return Math.round(total/10000)/100+'M';
            else if (total < 100000000) return Math.round(total/100000)/10+'M';
            else return Math.round(total/1000000)+'M';
        },
        getSalaryString: function(years, total) {
            if (!years || !total) return 'N/A';
            console.log(years,total);
            var fp = years+' Years $';
            fp = fp+this.roundSalary(total);
            console.log('fp',fp, fp.length);
            return fp.length === 0 ? 'N/A' : fp;
        },
        getHeightString: function(h) {
            return Math.floor(h/12)+"'"+h%12+'"';
        },
        getRecentSchool: function(h, c) {
            if (c == 'NULL' && h == 'NULL') return 'N/A';
            if (c == 'NULL') return h;
            return c;
        },
        getAgeInYears: function(y) {
            return Math.floor((new Date() - new Date(y).getTime()) / 3.15576e+10)
        },
        logoUrl: function(teamAbbrv) {
            return "https://pratyush.rustagi.cc/logos/"+teamAbbrv+".png";
        },
    },
    beforeRouteUpdate(to, from, next) {
        this.fetchPlayer();
        next();
    },
    watch: {
        $route (to, from) {
            this.fetchPlayer();
        }
    },
    created() {
        this.fetchPlayer();
    }
}
</script>
