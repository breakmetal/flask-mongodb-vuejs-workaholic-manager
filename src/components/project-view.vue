<template>
  <v-container fluid>
    <div>
    <v-app-bar
      color="deep-purple accent-4"
      dense
      dark
    >
      <v-toolbar-title>Add task</v-toolbar-title>
      <v-btn icon @click="dialogAdd=true">
        <v-icon>note_add</v-icon>
      </v-btn>
      <v-spacer></v-spacer>

      

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-menu
        left
        bottom
      >
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item
            v-for="n in 5"
            :key="n"
            @click="() => {}"
          >
            <v-list-item-title>Option {{ n }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-dialog v-model="dialogAdd" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">add task</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row justify="center">
                  <v-col cols="12" sm="8" md="8">
                    <v-text-field v-model="editedItem.title" label="title"></v-text-field>
                  </v-col>
                </v-row>
                <v-row justify="center">
                  <v-col cols="12" sm="8" md="8">
                    <v-text-field v-model="editedItem.description" label="description"></v-text-field>
                  </v-col>
                </v-row>
                <v-row justify="center">
                  <v-date-picker v-model="editedItem.date_limit"></v-date-picker>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <!--dialgo for sub tasks-->

         <v-dialog v-model="dialogSubTask" max-width="500px">
          <v-card>
            <v-card-title>
              <span class="headline">add sub-task</span>
            </v-card-title>
            <v-card-text>
              <v-container>
                <v-row justify="center">
                  <v-col cols="12" sm="8" md="8">
                    <v-text-field v-model="formSubTask.title" label="title"></v-text-field>
                  </v-col>
                </v-row>
                <v-row justify="center">
                  <v-col cols="12" sm="8" md="8">
                    <v-text-field v-model="formSubTask.description" label="description"></v-text-field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <div class="flex-grow-1"></div>
              <v-btn color="blue darken-1" text @click="dialogSubTask=false">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="addSubTask">Save</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <!--dialgo for sub tasks-->
  </div>
    <v-data-iterator
      :items="tasks"
      :items-per-page.sync="itemsPerPage"
      :footer-props="{ itemsPerPageOptions }"
    >
      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="item in props.items"
            :key="item.name"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card>
              <v-card-title class="blue white--text">
                <span class="headline">{{item.title}}</span>
                <v-spacer></v-spacer>
                <v-menu bottom left>
                  <template v-slot:activator="{ on }">
                    <v-btn
                      dark
                      icon
                      v-on="on"
                    >
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                <v-list>
                  <v-list-item >update</v-list-item>
                  <v-list-item @click=" prevDelete(item)">delete</v-list-item>
                </v-list>
          </v-menu>
        </v-card-title>

              <v-list-item-content class="align-start"> created_at: {{ item.created_at.$date }}</v-list-item-content>
              <v-list-item-content class="align-start"> date_limit: {{ item.date_limit }}</v-list-item-content>
              <v-divider></v-divider>
              <v-card-text>{{ item.description }}</v-card-text>
              <v-list dense>
                <v-list-item>
                  <v-img src="https://picsum.photos/510/300?random" aspect-ratio="1.7" contain></v-img>
                </v-list-item>
              </v-list>
              <v-list dense  v-for="subTask in item.subTasks"
            :key="subTask.name">
            <v-divider></v-divider>
            <v-divider></v-divider>
                <v-list-item>
                  <v-card-title >{{ subTask.title}}</v-card-title>
                </v-list-item>
                  <v-list-item>
                  <v-card-text class="align-end">{{ subTask .description }}</v-card-text>
                </v-list-item>
              </v-list>
             <v-card-actions>
              <v-btn
                color="deep-purple accent-4"
                text
                @click="prevSubTask(item)"
              >
                Add sub-task
              </v-btn>
            </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>
import axios from 'axios'
  export default {
    data: () => ({
      dialogSubTask:false,
      formSubTask:{
        title:'',
        description:'',
        idTask:''
      },
      idProject:'',
      editedIndex:-1,
      editedItem:{},
      defaultItem: {},
      dialogAdd:false,
      tasks: [],
      itemsPerPageOptions: [4, 8, 12],
      itemsPerPage: 4,
    }),
    created () {
      this.idProject = this.$route.params.id
      this. getTasks(this.idProject)
    },
    methods: 
    {
      getTasks(id){
        axios({ method: 'GET', url: `http://127.0.0.1:5000/api/task/${id}` }).then(
          result => {
                      console.log(result.data)
                      this.tasks = result.data
                    },
          error => {
            console.error(error)
          })
        },
        close () {
        this.dialogAdd = false
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      },
      editItem (item) {
            this.editedItem = Object.assign({}, item)
            this.dialogAdd = true
            this.editedIndex = this.tasks.indexOf(item)
            alert(this.editedItem.project_id.$oid)
      },
      save () {
        this.editedItem.project_id = this.idProject
        if (this.editedIndex == -1) {
          axios.post(`http://127.0.0.1:5000/api/add_task`,this.editedItem).then(
            result => {
               this.getTasks(this.idProject)
                console.log(result)
          }).catch(err => {
              console.log(err)
          })
        } else {
          this.id = this.editedItem._id.$oid
          axios.put(`http://127.0.0.1:5000/api/update_task/${this.id}`,this.editedItem).then(
            result => {
                this.isEdit = false
                this.getTasks()
                console.log(result)
        }).catch(err => {
            console.log(err)
        })

        }
       
        this.close() 
      },
      addSubTask(item){
        axios.post(`http://127.0.0.1:5000/api/add_sub_task`,this.formSubTask).then(
            result => {
               this.getTasks(this.idProject)
                console.log(result)
          }).catch(err => {
              console.log(err)
          })
          this.dialogSubTask = false
      },
      prevSubTask(item){
        this.formSubTask.idTask = item._id.$oid
        this.dialogSubTask = true
      },
      prevDelete(item){
        this.editedItem = Object.assign({}, item)
        this.deleteItem()
      },
      deleteItem () {
        this.id = this.editedItem._id.$oid
        axios({ method: 'DELETE', url: `http://127.0.0.1:5000/api/delete_task/${this.id}` }).then(
                result => {
                            console.log(result.data)
                            this.getTasks(this.idProject)

                },
            error => {
                console.error(error)
            })
        this.alertDelete = false
      },
      },
     
    }
</script>

