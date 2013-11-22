/*                                                                            */
/* File Name..........: ~/scripts/dummy_program.cc
 * Author.............: Bjorn Barrefors
 * Institution........: University of Nebraska-Lincoln
 * ...................: Department of Computer Science and Engineering
 * Date Written.......: October 1, 2012
 * Date Last Modified.: November 1, 2012
 * Language...........: C++
 * Purpose............: To run in the background and cause higher power usage
 * Brief Description..: Counts from 0 to 1000001 over and over again.
 * ...................: If loop hits 1000002 the program will terminate.
 * ...................: This will never happen because if the loop goes past
 * ...................: 1000000 it is reset to 0.
 * Improvements.......: 
 */

int main (int argc, char *argv[]) {
  int count = 0;
  while (count < 1000002)
    {
      count++;
      if (count > 1000000)
	count = 0;
    }
  return 0;
}
