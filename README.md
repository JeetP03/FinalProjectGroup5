# **NinerNexus**
---
## Introduction

This application gives UNCC students a simple platform to communicate exclusively with other students via photo, video and text based posts. Users will have the ability to create their own profiles where they can view their posts, number of likes, what users they follow and their own followers. They will also be able to view a feed based on who they follow and who they engage with most.

## Problem Statement
Currently, there is no explicit web application where students of UNCC can communicate with each other through photo, video, or text. NinerNexus will help with this in that it will allow students to inform each other about ongoing events on campus, help each other with course related work, or even to meet new people and make new friends. 

## Target Audience
The target audience for our application are UNCC students looking to build connections with other fellow students. The application provides an opportunity to look for people with similar interests. 

## Requirements
### Functional Requirements
 - Open a new account
 - Set username and password for an account
 - Post a text post
 - Post a photo post
 - Post a video post
 - View an user account page
   **This includes:**
    - Their own posts
    - Their own user and post statistics
    - Saved Posts
    - User basic information
  - View a user feed
   **This includes:**
    - Displays posts from users that the user follows
   - Orders posts based on a highest engagement-level first policy
![Requirements Part 1t](https://github.com/JeetP03/FinalProjectGroup5/blob/main/Images/SEFPPG5-RequirementsDiagrams_1.png)

![Requirements Part 2 ](https://github.com/JeetP03/FinalProjectGroup5/blob/main/Images/SEFPPG5-RequirementsDiagrams_2.png)

### Non-Functional Requirements
 - Users cannot post copyrighted material
 - Users cannot post material deemed inappropriate
 - A page must load within 3 seconds
 - Database data must be updated within 3 seconds
 - Users must be prompted to login upon each launching of the web app
 - System must be able to support 30 visitors at a time


## Software Architecture
Some of the major components of the application is being able to post, like, and comment. Whenever a user posts any content or comments on an existing post, it is stored in the HTML files and displayed to the public. Whenever a user likes a post, the data is stored in an SQL file and displayed via Pyhton. 
![Architecture](https://github.com/JeetP03/FinalProjectGroup5/blob/main/Images/Screenshot%202023-03-24%20183406.png)

## Technology Stack
## Front End Technology for User Interface
- HTML
- CSS
- Bootstrap

 ## Back End Technology
- Python
- mySQL
- Flask

## Team Members
- Bhuvi Alluri
- Jeet Patel
- Daniel Santos
- Sri Gade



