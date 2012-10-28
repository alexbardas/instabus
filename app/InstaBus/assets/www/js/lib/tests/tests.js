'use strict'

var should = chai.should();

describe('Utils', function(){
 	describe('#degreeToRadians()', function(){
  		it('should convert degrees into radians', function() {
  			Utils.degreeToRadians(0).should.equal(0);
			Utils.degreeToRadians(90).should.equal(Math.PI/2);
			Utils.degreeToRadians(180).should.equal(Math.PI);
		})
	});
	describe('#getClosestStations()', function(){
  		it('should get the closest stations near a point, given a list of stations', function() {
  			Utils.getClosestStations(new Point(44, 25), []).should.be.an('array');
		})
	});
	describe('#getStationPriority()', function(){
  		it('should return the priority of a station', function() {
  			Utils.getStationPriority({linii:{"a":"162, 163, N110","t":11}}).should.equal(4);
  			Utils.getStationPriority({linii:{"a":"162, 163, N110","m":"15, 27","t":11}}).should.equal(6);
		})
	});
});

describe('PriorityQueue', function(){
 	describe('#add()', function(){
  		it('should add some items to the queue, and keep them sorted', function() {
  			var q = new PriorityQueue(5);
  			q.add(1, 4);
  			q.add(2, 3);
  			q.add(3, 2);
  			q.add(4, 5);
  			q.add(5, 3);
  			q.add(6, 7);
  			q.getItems().should.eql([6,4,1,2,5]);
		});
		it('should create a queue with max_length = 3', function() {
  			var q = new PriorityQueue(3);
  			q.add(25, 1);
  			q.add(2, 2);
  			q.add(3, 17);
  			q.add(4, 4);
  			q.add(5, 5);
  			q.add(6, 1);
  			q.getItems().should.eql([3,5,4]);
		})
	});
});
describe('#getStations()', function () {
    it('should retrieve the correct station by id', function () {
        Utils.getStation(1).nume.should.eql('Grozavesti');
    });
});
