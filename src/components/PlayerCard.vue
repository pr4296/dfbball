<template>
    <div>
        {{ player.firstName }}
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
            // console.log('inside Team fetchTeam');
            var url = 'https://pratyush.rustagi.cc/dfbball/api/playerInfo.php?playerId='+this.$route.params.playerId;
            // console.log(url);
            fetch(url)
                .then(function(response) {return response.json()})
                .then(function(responseData) {
                    console.log(responseData);
                    player = responseData;
            });
        },
    }
}
</script>
