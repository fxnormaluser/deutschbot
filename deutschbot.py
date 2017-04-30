from piston.steem import Steem
from piston.blockchain import Blockchain

chain = Blockchain()

blacklist = [""]   

trusted_voters = [""]   

pk = ["postingkeyhere"] 

account = ["deutschbot"]

threshold = 1 

steem = Steem(keys=pk[0])) 

for operation in chain.ops(
                           filter_by=["vote"]
                          ):

    op = operation["op"]

    if op[0] == "vote":

        comment_voter = op[1]["voter"]

        if comment_voter in trusted_voters:

            comment_link = op[1]["permlink"]
            comment_author = op[1]["author"]
            vote_weight = int(op[1]["weight"]/100)
            timestamp = operation["timestamp"]
            if not "/re-" in comment_link:
                comment = steem.get_post("@" + comment_author + "/" + comment_link)
                tags = (comment["json_metadata"].get("tags", []))
                category = comment.category
        
                if comment.is_main_post(): 

                       if "deutsch" in tags or "deutsch" in category:

                        if not comment_author in blacklist:

                            print(timestamp + " vote by: " + comment_voter + " for " + comment_link + " weight:" + str(vote_weight)) 
                            counter = 1

                            for avote in comment['active_votes']:

                                if avote['voter'] in trusted_voters and not avote['voter'] == comment_voter:

                                    print(avote['voter'] + " also liked it")                        
                                    counter = counter + 1
                            
                            if counter > threshold:
                          
                                for (k,v) in enumerate(account): 

                                    already_voted = False

                                    for avote in comment['active_votes']:
                                            
                                        if (avote['voter'] == v):

                                            already_voted=True                                       

                                    if not already_voted == True:

                                        try:

                                          steem = Steem(keys=pk[k], node="wss://gtg.steem.house:8090")
                                          comment.vote(100, v) 
                                          print("... followed with " + v + " with 100%")

                                        except Exception as e:

                                          print("... NOT followed with " + v + " because:")
                                          print(str(e))
