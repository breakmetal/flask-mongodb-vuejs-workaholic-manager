import Vue from 'vue'
import Router from 'vue-router'
//import Home from '@/components/Home'
import index from '@/components/index'
import ListProjects from '@/components/projects'
import projectView from '@/components/project-view'




Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
        path: '/index',
        name: 'index',
        component: index
    },
    {
      path: '/proyects',
      name: 'ListProjects',
      component: ListProjects
    },
    {
      path: '/project-view/:id',
      name: 'project-view',
      component: projectView
    },
   
  ]
})
