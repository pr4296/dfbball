<template>
    <div>
        {{ player.firstName }}
        abcdefghijkljsdf
    </div>
</template>

<script>
import store from "@/store.js";
import router from "@/router.js";

export default {
    name: "PlayerCard",
    props: ['playerId'],
    data: function() {
        return {
            player: {}
        }
    },
    methods: {
        fetchPlayer: function() {
            console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerInfo.php?id='+this.$route.params.id;
            console.log(url);
            var vm = this;
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    // console.log()
                    vm.player = responseData;
            });
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
