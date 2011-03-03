import redis


class node:
	def __init__(self, thisKey, next):
		self.__thisKey = thisKey
		self.__next = next

	def setNext(self, next):
		self.__next = next

        def getNext(self):
                return self.__next

        def getThisKey(self):
                return self.__thisKey


class LinkedListRedis:

	def __init__(self, url='localhost', port=6379):
		self.__redis = redis.Redis(host=url, port=port, db=0)
		self.__head = False
		self.__tail = False

        def set(self, k, v, ttl=60):
                n = node (k, False)
                if (self.__head == False):
                        self.__head = n
                        self.__tail = n
                else:
                        self.__tail.setNext(n)
                        self.__tail = n

                self.__redis.set(k, v)
		self.__redis.expire(k, ttl);


        def get(self, k):
                if (self.__head == False):
                        return False

                # setup nodes for linear scan
                currNode = self.__head
                lastNode = self.__head

                while (currNode != False):
			
                        # delete curr and relink if curr key has expired
                        if self.__redis.get(currNode.getThisKey()) == None:

				self.__delete(currNode, lastNode)
				if currNode.getThisKey() == k:
					break
				if lastNode.getNext() != False:
					currNode = lastNode
				if (lastNode.getNext()==False) and (
				    currNode.getNext()==False):
					currNode = self.__head
					lastNode = self.__head
					continue
					
                        # check if key is found
                        if currNode.getThisKey() == k:
                                val = self.__redis.get(currNode.getThisKey())
                                if val == None:
                                        val = False
                                return val
				
			
			# setup for next iteration
                        lastNode = currNode
                        currNode = currNode.getNext()
		
		return False


	def __delete(self, currNode, lastNode):
		#case 1: list has 1 node
		if (currNode.getNext()==False) and (
		     lastNode.getNext()==False):
			self.__head = False
			self.__tail = False

		#case 2: removing 1st node
		elif lastNode == currNode:
			self.__head = lastNode.getNext()
			lastNode.setNext(False)

		#case 3: removing last node
		elif currNode.getNext() == False:
			lastNode.setNext(False)
			self.__tail = lastNode

		#case 4: removing from middle
		else:
			lastNode.setNext(currNode.getNext())


	def dele(self, k):
		# return if list is empty 
		if (self.__head == False):
			return False

		# setup nodes for linear scan
		currNode = self.__head
		lastNode = self.__head

                while (currNode != False):

			# found node to delete
                        if currNode.getThisKey() == k:
				
				# call function to delete curr node
				self.__delete(currNode, lastNode)
				
				#delete from redis
				self.__redis.delete(k)

				# return True, i.e., del success
				return True
					
			# setup for next iteration
			lastNode = currNode
                        currNode = currNode.getNext()

                return False


        def cleanup(self):
                if (self.__head == False):
                        return False

                # setup nodes for linear scan
                currNode = self.__head
                lastNode = self.__head

                while (currNode != False):

                        # delete curr and relink if curr key has expired
                        if self.__redis.get(currNode.getThisKey()) == None:
                                self.__delete(currNode, lastNode)
                                if lastNode.getNext() != False:
                                        currNode = lastNode
                                if (lastNode.getNext()==False) and (
                                    currNode.getNext()==False):
                                        currNode = self.__head
                                        lastNode = self.__head
                                        continue

                        # setup for next iteration
                        lastNode = currNode
                        currNode = currNode.getNext()

                return False


	def stats(self):
		keyDump = ""
		currNode = self.__head
		while (currNode != False):
			keyDump += currNode.getThisKey() + ":"
			keyDump += str(self.__redis.ttl(currNode.getThisKey()))
			keyDump += ";"
			currNode = currNode.getNext()
		print keyDump;



