'use strict'

var should = chai.should();

describe('Utils', function(){
 	describe('#degreeToRadians()', function(){
  		it('should convert degrees into radians', function() {
  			Utils.degreeToRadians(0).should.equal(0);
			Utils.degreeToRadians(90).should.equal(Math.PI/2);
			Utils.degreeToRadians(180).should.equal(Math.PI);
		})
	})
	describe('#getClosestStations()', function(){
  		it('should get the closest stations near a point, given a list of stations', function() {
  			Utils.getClosestStations(new Point(44, 25), []).should.be.an('array');
		})
	})
});