<template>
  
  <div id="app" ondragstart="return false">

    <div class="board">
      <button @click="sync">sync</button>
      <button @click="newgame">new</button>
      <button @click="getuser">getuser</button>
      <div v-for="(_,rank) in 8" :key="rank" class="rank">
        <div v-for="(_,file) in 8" :key="rank * 8 + file" 
          :class="{
            square: true, 
            black:(rank+file)%2 == 1,
            selected: selected[hash(rank,file)]
            }"
          @mouseup="clicked(rank,file)"
          @unselect="unselect($event)"
          >
          <div v-if="getPiece(rank,file)" :class="['piece',getPiece(rank,file).name,getPiece(rank,file).color == 1 ? 'black':'']">
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import axios from "axios"
export default {
  name: 'App',
  data(){
    return {
      selected: {},
      message: {},
      bodykeys: ["rank","file","xto","yto"],
      board: {}
    }
  },
  methods:{
    getPiece(rank,file){
      //this structure is insanely fragile, rework when possible
      let p = this.board[`(${rank}, ${file})`]
      return p
    },
    clicked(rank,file){
      this.$set(this.selected,this.hash(rank,file),true)
      let len = Object.keys(this.message).length
      this.message[this.bodykeys[len]] = file
      this.message[this.bodykeys[len+1]] = rank

      if(Object.keys(this.selected).length == 2){
        this.sendmove(this.message)
        .then(res=>console.log(res))
        .then(()=>this.sync())
        .catch((err)=>console.log(err))
        this.selected = {}
        this.message = {}
      }
    },
    basic_request(endpoint,data){
        return fetch('http://localhost:5000/'+endpoint,{
          method: 'POST', // *GET, POST, PUT, DELETE, etc.
          mode: 'cors', // no-cors, *cors, same-origin
          cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',
          },
          redirect: 'follow', // manual, *follow, error
          referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
          body: JSON.stringify(data) // body data type must match "Content-Type" header
        })
        .then(res=>{
          console.log(res)
          return res
        })
        .then(res=>res.json())
      
    },
    sendmove(move){
      return this.basic_request('move',move)
    },
    sync(){
      this.basic_request('sync',{}).then(board=>{
        this.board = board
      });
    },
    newgame(){
      return this.basic_request('newgame',{}).then(()=>this.sync())
    },
    getuser(){
      return this.basic_request('getuser',{})
    },
    hash(rank,file){
      return rank*8+file
    }
  }
}
</script>

<style lang='scss' scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}


.board{
  /*  */
  height: auto;
  display: inline-block;
}
.rank{
  margin: 0;
  padding: 0;
  display: flex;
}

.square{
  background-color: rgb(247, 212, 166);
  min-height: 10vw;
  min-width: 10vw;
  max-height: 10vw;
  max-width: 10vw;
  display: inline-block;
  box-sizing: border-box;
}

.black{
  background-color:#8a561f;
}
.selected{
  border: 3px solid;
  box-shadow: inset;
  border-color: greenyellow;
}
.allpieces{
  background: url('assets/pieces.png');
  width: 300px;
  height: 100px;
  background-repeat: no-repeat;
}
.piecetest{
  display: grid;
  width: 50px;
  grid-template-rows: repeat(6, 20px);
  grid-template-columns: repeat(2,20px);
  grid-auto-flow: column;
}
.piece{
  position: relative;
  left:0;
  width: 100%;
  height: 100%;
  background: url('assets/pieces.png');
  background-repeat: no-repeat;  
  background-size: 580% auto;
  &.king{
    background-position-x: 0%;
  }
  &.queen{
    background-position-x: 20%;
  }
  &.bishop{
   background-position-x: 40%;
  }
  &.knight{
    background-position-x: 60%;
  }
  &.rook{
    background-position-x: 80%;
  }
  
  &.pawn{
    background-position-x: 100%;
  }
  &.black{
    background-position-y: 105%;
  }
}

</style>
