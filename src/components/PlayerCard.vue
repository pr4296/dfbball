<template>
    <div class="card boxShadow">
        <div class="statBox">
            <h2>{{ this.player.firstName }} {{this.player.lastName }}</h2>
            <img class="playerCardImage" :src="this.player.imgUrl"/>
            <span>Jersey #{{ this.player.jerseyNumber }}</span>
            <span>{{ getFullPositionName(this.player.primaryPosition) }}</span>
            <span>{{ getSalaryString(this.player.contractYearsCount, this.player.contractTotalSalary)}}</span>
            <span>{{ getHeightString(this.player.heightInches)}}  {{this.player.weightPounds}} lbs</span>
            <span>{{ getRecentSchool(this.player.highSchool, this.player.college)}}</span>
            <span>{{ getAgeInYears(this.player.birthDate)}}</span>
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
            if (!years || !total) return '';
            console.log(years,total);
            var fp = years+' Years $';
            return fp+this.roundSalary(total);
        },
        getHeightString: function(h) {
            return Math.floor(h/12)+"'"+h%12+'"';
        },
        getRecentSchool: function(h, c) {
            if (c == 'NULL' && h == 'NULL') return '';
            if (c == 'NULL') return h;
            return c;
        },
        getAgeInYears: function(y) {
            return 'Born '+y+' - '+Math.floor((new Date() - new Date(y).getTime()) / 3.15576e+10)+' Years Old';
        }
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
